from datetime import datetime, timedelta
from sqlalchemy import func, desc
from src.models import Match, Team, Player, GuestPlayer, Goal, News, Notification, Court, MVPVote, User
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
                        message=f"Has jugado un nuevo partido ({result}) - {match_date.strftime('%d/%m/%Y')}. Tenés 24 horas para votar al jugador del partido.",
                        match_id=match_id
                    )
                    db.session.add(noti)
            db.session.commit()
        except Exception as e:
            print(f"Error creando notificaciones post-partido: {e}")
            db.session.rollback()

    @staticmethod
    def register_mvp_vote(match_id, voter_player_id, voted_player_id):
        """
        Registra un voto al MVP validando:
        - votante participante del partido,
        - objetivo participante del partido,
        - no auto-voto,
        - solo un voto por jugador y partido,
        - ventana de 24h vigente.
        """
        match = Match.query.get(match_id)
        if not match:
            return False, "Partido no encontrado"

        if match.mvp_id is not None:
            return False, "La votación ya finalizó para este partido"

        if datetime.utcnow() > match.get_mvp_voting_deadline():
            MatchService.finalize_expired_mvp_votes()
            return False, "La ventana de votación (24 horas) ya venció"

        if voter_player_id == voted_player_id:
            return False, "No podés votarte a vos mismo"

        participant_ids = {player.id for player in match.players}
        if voter_player_id not in participant_ids:
            return False, "Solo pueden votar jugadores que participaron del partido"

        if voted_player_id not in participant_ids:
            return False, "Solo se puede votar a jugadores que participaron del partido"

        existing_vote = MVPVote.query.filter_by(
            match_id=match_id,
            voter_player_id=voter_player_id
        ).first()
        if existing_vote:
            return False, "Ya registraste tu voto para este partido"

        try:
            vote = MVPVote(
                match_id=match_id,
                voter_player_id=voter_player_id,
                voted_player_id=voted_player_id
            )
            db.session.add(vote)
            db.session.commit()
            return True, "Voto registrado correctamente"
        except Exception:
            db.session.rollback()
            return False, "Ocurrió un error al registrar tu voto"

    @staticmethod
    def finalize_expired_mvp_votes():
        """
        Cierra votaciones vencidas (24h), calcula MVP, crea noticia y notifica a votantes.
        Es idempotente: un partido con mvp_id definido no se reprocesa.
        """
        now = datetime.utcnow()
        expired_matches = Match.query.filter(
            Match.mvp_id.is_(None),
            Match.date <= now - timedelta(hours=24)
        ).all()

        if not expired_matches:
            return 0

        finalized_count = 0

        for match in expired_matches:
            participant_ids = [player.id for player in match.players]
            if not participant_ids:
                continue

            vote_counts = db.session.query(
                MVPVote.voted_player_id,
                func.count(MVPVote.id).label('total_votes')
            ).filter(
                MVPVote.match_id == match.id
            ).group_by(
                MVPVote.voted_player_id
            ).order_by(
                desc('total_votes'),
                MVPVote.voted_player_id.asc()
            ).all()

            winner_player_id = None
            winner_votes = 0

            if vote_counts:
                winner_player_id = vote_counts[0].voted_player_id
                winner_votes = vote_counts[0].total_votes
            else:
                # Fallback en caso de no haber votos: máximo goleador registrado del partido.
                top_scorer = db.session.query(
                    Goal.player_id,
                    func.count(Goal.id).label('goals')
                ).filter(
                    Goal.match_id == match.id,
                    Goal.player_id.isnot(None)
                ).group_by(
                    Goal.player_id
                ).order_by(
                    desc('goals'),
                    Goal.player_id.asc()
                ).first()

                if top_scorer:
                    winner_player_id = top_scorer.player_id
                else:
                    winner_player_id = sorted(participant_ids)[0]

            winner = Player.query.get(winner_player_id)
            if not winner:
                continue

            match.mvp_id = winner_player_id

            title = "Jugador del Partido"
            if winner_votes > 0:
                content = (
                    f"Finalizó la votación del partido del {match.date.strftime('%d/%m/%Y')} "
                    f"y el jugador del partido fue {winner.name} {winner.surname} con {winner_votes} voto(s)."
                )
            else:
                content = (
                    f"Finalizó la ventana de votación del partido del {match.date.strftime('%d/%m/%Y')} "
                    f"y el jugador del partido fue {winner.name} {winner.surname}."
                )

            system_user = User.query.filter_by(is_admin=True).first() or User.query.first()
            if not system_user:
                continue

            news = News(
                title=title,
                content=content,
                user_id=system_user.id,
                player_id=winner_player_id,
                court_id=match.court_id,
                match_id=match.id
            )
            db.session.add(news)

            voter_ids = db.session.query(MVPVote.voter_player_id).filter(
                MVPVote.match_id == match.id
            ).distinct().all()

            for voter_tuple in voter_ids:
                voter_player = Player.query.get(voter_tuple[0])
                if voter_player and voter_player.user:
                    db.session.add(Notification(
                        user_id=voter_player.user.id,
                        message=f"Se cerró la votación del partido {match.result}. MVP: {winner.name} {winner.surname}.",
                        match_id=match.id
                    ))

            finalized_count += 1

        if finalized_count > 0:
            db.session.commit()

        return finalized_count
