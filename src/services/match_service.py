from datetime import datetime
from src.models import Match, Team, Player, GuestPlayer, Goal, News, Notification, Court
from config.database import db

class MatchService:
    @staticmethod
    def create_match(match_date, match_type, court_id, team_a_players, team_a_guests, 
                     team_b_players, team_b_guests, goals_data, user_id):
        """
        Crea un partido con todos sus componentes de forma transaccional.
        Retorna (match_id, error_message). Si error_message es None, fue exitoso.
        """
        try:
            # Calcular resultado
            score_a = len([g for g in goals_data if g['team'] == 'A'])
            score_b = len([g for g in goals_data if g['team'] == 'B'])
            result = f"{score_a}-{score_b}"

            # 1. Crear el partido
            match = Match(date=match_date, match_type=match_type, court_id=court_id, result=result)
            db.session.add(match)
            db.session.flush() # Flush para obtener match.id

            # 2. Crear equipos
            team_a = Team(team_name='A', match_id=match.id, score=score_a)
            team_b = Team(team_name='B', match_id=match.id, score=score_b)
            db.session.add(team_a)
            db.session.add(team_b)
            db.session.flush()
            
            # 3. Asignar jugadores Team A
            for player_id in team_a_players:
                player = Player.query.get(int(player_id))
                if player:
                    team_a.players.append(player)
                    if player not in match.players:
                        match.players.append(player)

            for guest_name in team_a_guests:
                guest = GuestPlayer(name=guest_name)
                db.session.add(guest)
                team_a.guest_players.append(guest)
                match.guest_players.append(guest)

            # 4. Asignar jugadores Team B
            for player_id in team_b_players:
                player = Player.query.get(int(player_id))
                if player:
                    team_b.players.append(player)
                    if player not in match.players:
                        match.players.append(player)

            for guest_name in team_b_guests:
                guest = GuestPlayer(name=guest_name)
                db.session.add(guest)
                team_b.guest_players.append(guest)
                match.guest_players.append(guest)

            db.session.flush()

            # 5. Registrar Goles
            for goal_data in goals_data:
                team_id = team_a.id if goal_data['team'] == 'A' else team_b.id
                
                if goal_data['scorer_type'] == 'player':
                    goal = Goal(match_id=match.id, team_id=team_id, player_id=int(goal_data['scorer_id']))
                    db.session.add(goal)
                else:
                    guest_name = goal_data['scorer_name']
                    guest_players = team_a.guest_players if goal_data['team'] == 'A' else team_b.guest_players
                    guest = next((g for g in guest_players if g.name == guest_name), None)
                    if guest:
                        goal = Goal(match_id=match.id, team_id=team_id, guest_player_id=guest.id)
                        db.session.add(goal)

            # 6. Commit de toda la transacción principal
            db.session.commit()

            # 7. Disparar acciones secundarias (News, Notifications)
            MatchService._create_news_and_notifications(match.id, match_type, match_date, court_id, result, user_id, team_a_players + team_b_players)

            return match.id, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def _create_news_and_notifications(match_id, match_type, match_date, court_id, result, user_id, all_player_ids):
        try:
            court = Court.query.get(court_id)
            court_name = court.name if court else "Cancha"
            news_title = f"🏆 Nuevo Partido Registrado - {match_type}"
            news_content = f"Se ha registrado un nuevo partido de {match_type} el {match_date.strftime('%d/%m/%Y')} en {court_name}. Resultado final: {result}. ¡Felicitaciones a todos los participantes!"
            
            news = News(title=news_title, content=news_content, user_id=user_id, court_id=court_id, match_id=match_id)
            db.session.add(news)

            all_registered_players = []
            for pid in all_player_ids:
                p = Player.query.get(int(pid))
                if p and p not in all_registered_players:
                    all_registered_players.append(p)

            for player in all_registered_players:
                if player.user:
                    noti = Notification(
                        user_id=player.user.id,
                        message=f"Has jugado un nuevo partido ({result}) - {match_date.strftime('%d/%m/%Y')}",
                        match_id=match_id
                    )
                    db.session.add(noti)
            db.session.commit()
        except Exception as e:
            print(f"Error creando notificaciones post-partido: {e}")
            db.session.rollback()
