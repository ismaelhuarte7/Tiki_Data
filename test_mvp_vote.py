"""
Test de la funcionalidad MVP Vote
Simula un partido con votaciones y verifica el flujo completo.
"""
from datetime import datetime, timedelta, timezone
from app import app
from config.database import db
from src.models import Match, Player, User, Court, Team, Notification, MVPVote, News
from src.services.match_service import MatchService


def test_mvp_voting_flow():
    """Test completo del flujo de votaciones MVP"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("INICIANDO TEST DE VOTACIÓN MVP")
        print("="*60)
        
        players = Player.query.limit(4).all()
        if len(players) < 4:
            print("ERROR: Se necesitan al menos 4 jugadores. Ejecuta el seed primero.")
            return
        
        court = Court.query.first()
        if not court:
            print("ERROR: No hay canchas. Crea una primero.")
            return
        
        print(f"\n1. Jugadores disponibles: {[p.name + ' ' + p.surname for p in players]}")
        print(f"   Cancha: {court.name}")
        
        match_date = datetime.now(timezone.utc) - timedelta(hours=2)
        
        match = Match(
            date=match_date,
            match_type='5',
            result='3-2',
            court_id=court.id
        )
        db.session.add(match)
        db.session.flush()
        
        team_a = Team(team_name='A', match_id=match.id, score=3)
        team_b = Team(team_name='B', match_id=match.id, score=2)
        db.session.add_all([team_a, team_b])
        db.session.flush()
        
        team_a.players.extend([players[0], players[1]])
        team_b.players.extend([players[2], players[3]])
        match.players.extend(players)
        
        db.session.commit()
        
        print(f"\n2. Partido creado: ID={match.id}")
        print(f"   Fecha: {match.date}")
        print(f"   Resultado: {match.result}")
        print(f"   Participantes: {len(match.players)} jugadores")
        
        for player in players:
            if player.user:
                noti = Notification(
                    user_id=player.user.id,
                    message=f"Has jugado un nuevo partido ({match.result}). Tenes 24 horas para votar al jugador del partido.",
                    match_id=match.id
                )
                db.session.add(noti)
        db.session.commit()
        
        print(f"\n3. Notificaciones creadas: {len(Notification.query.filter_by(match_id=match.id).all())}")
        
        print(f"\n4. Verificando votacionabierta:")
        print(f"   - mvp_id: {match.mvp_id}")
        print(f"   - deadline: {match.get_mvp_voting_deadline()}")
        print(f"   - is_open: {match.is_mvp_voting_open()}")
        
        print(f"\n5. Registrando votaciones:")
        
        success, msg = MatchService.register_mvp_vote(match.id, players[0].id, players[1].id)
        print(f"   - {players[0].name} vota a {players[1].name}: {msg}")
        
        success, msg = MatchService.register_mvp_vote(match.id, players[1].id, players[0].id)
        print(f"   - {players[1].name} vota a {players[0].name}: {msg}")
        
        success, msg = MatchService.register_mvp_vote(match.id, players[2].id, players[0].id)
        print(f"   - {players[2].name} vota a {players[0].name}: {msg}")
        
        success, msg = MatchService.register_mvp_vote(match.id, players[3].id, players[2].id)
        print(f"   - {players[3].name} vota a {players[2].name}: {msg}")
        
        print(f"\n6. Verificando validacion (auto-voto debe fallar):")
        success, msg = MatchService.register_mvp_vote(match.id, players[0].id, players[0].id)
        print(f"   - Auto-voto: {msg}")
        
        print(f"\n7. Verificando validacion (segundo voto debe fallar):")
        success, msg = MatchService.register_mvp_vote(match.id, players[0].id, players[1].id)
        print(f"   - Segundo voto: {msg}")
        
        print(f"\n8. Votos registrados: {MVPVote.query.filter_by(match_id=match.id).count()}")
        for vote in MVPVote.query.filter_by(match_id=match.id).all():
            print(f"   - {vote.voter.name} -> {vote.voted_player.name}")
        
        print(f"\n9. Finalizando votaciones expiradas...")
        
        match.date = datetime.now(timezone.utc) - timedelta(hours=25)
        db.session.commit()
        
        finalized = MatchService.finalize_expired_mvp_votes()
        print(f"   - Partidos finalizados: {finalized}")
        
        match = db.session.get(Match, match.id)
        print(f"\n10. RESULTADO:")
        print(f"    - MVP elegido: {match.mvp.name} {match.mvp.surname}" if match.mvp else "    - Sin MVP")
        
        print(f"\n11. Noticias creadas: {News.query.filter_by(match_id=match.id).count()}")
        for news in News.query.filter_by(match_id=match.id).all():
            print(f"    - {news.title}")
        
        voter_notifications = Notification.query.filter(
            Notification.match_id == match.id,
            Notification.message.like('%MVP%')
        ).count()
        print(f"\n12. Notificaciones a voters: {voter_notifications}")
        
        print("\n" + "="*60)
        print("TEST COMPLETADO")
        print("="*60 + "\n")


if __name__ == "__main__":
    test_mvp_voting_flow()