from django.urls import path
from .views.auth import signUp, authWithFortyTwo, signIn, logout, cookieToken, tfaSendMail, tfaSetActive
from django.conf import settings
from .views.player import (
    getInfoPlayer,
    editProfile,
    getPlayersList,
    changePassword,
    friends,
    readNotifications,
    dashboard
)
from .views.tournament import (
    createTournament,
    editTournament,
    getTournamentAvailable,
    joinTournament,
    alreadyInTournament,
    getUserTournament,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views.pong import (
    getMatchLocal,
)


urlpatterns = [
    # USER MANAGEMENT
    path('signUp', signUp.signUp, name='signUp'),
    path('authWithFortyTwo', authWithFortyTwo.authWithFortyTwo, name='authWithFortyTwo'),
    path('signIn', signIn.signIn, name='signIn'),
    path('playerLogout', logout.playerLogout, name='playerLogout'),
    # get refresh tokens and set them in Cookie
    path('refresh-token', cookieToken.CookieTokenRefreshView.as_view()),

    # GET USER INFO
	path('get-status',getInfoPlayer.PlayerStatus, name='PlayerStatus'),
    path('players', getPlayersList.PlayersList, name='playersList'),
    path('players/me', getInfoPlayer.PlayerView, name='playerView'),
    path('players/<uuid:pk>', getInfoPlayer.PlayerView, name='playerView'),

    # GET STATISTICS PER USER
    path('dashboard/<uuid:pk>', dashboard.DashboardView, name='dashboard'),
    path('tournamentsList/<uuid:pk>', dashboard.TournamentsList, name='tournamentsList'),
    path('matchList/<uuid:pk>', dashboard.MatchList, name='matchList'),

    # EDIT PROFILE
    path('change-password/<uuid:pk>', changePassword.ChangePassword, name='changePassword'),
    path('edit/<uuid:pk>', editProfile.EditProfile, name='edit'),
    path('change-status/<uuid:pk>', editProfile.ChangeStatus, name='changeStatus'),
	path('changeStatusRefresh/<uuid:pk>', editProfile.changeStatusRefresh, name='changeStatusRefresh'),
    
    # RELATIONS AND NOTIFICATIONS
    path('search', friends.SearchView, name='searchView'),
    path('friends/<uuid:pk>', friends.FriendsList, name='friends_list'),
    path('getuserid/<str:username>', friends.getUserIDbyUsername),
    path('send/<uuid:pk>', friends.SendFriendRequest, name='sendFriendRequest'),
    path('accept/<uuid:pk>', friends.AcceptFriendRequest, name='acceptFriendRequest'),
    path('reject/<uuid:pk>', friends.RejectFriendRequest, name='rejectFriendRequest'), # receiver can decline request
    path('cancel/<uuid:pk>', friends.CancelFriendRequest, name='cancelFriendRequest'), # sender can cancel his request
    path('unfriend/<uuid:pk>', friends.UnfriendView, name='unfriend'),
    path('fetch_all_notifications', readNotifications.fetch_all_notifications, name='fetch_all_notifications'),
    path('fetch_unread_notifications', readNotifications.fetch_unread_notifications, name='fetch_unread_notifications'),

    # TOURNAMENT
    path('createTournament', createTournament.createTournament, name='createTournament'),
    path('editTournament/<uuid:id>', editTournament.editTournament, name='editTournament'),
    path('getTournamentAvailable', getTournamentAvailable.getTournamentAvailable, name='getTournamentAvailable'),
    path('joinTournament', joinTournament.joinTournament, name='joinTournament'),
    path('alreadyInTournament', alreadyInTournament.alreadyInTournament, name='alreadyInTournament'),
    path('getUserTournament', getUserTournament.getUserTournament, name='getUserTournament'),

    # obtain tokens but not set them in Cookie()
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # TFA
    path('tfaSendMail/', tfaSendMail.tfaSendMail, name='tfaSendMail'),
    path('tfaSetActive/', tfaSetActive.tfaSetActive, name='tfaSetActive'),

    path('getMatchLocal/', getMatchLocal.getMatchLocal, name='getMatchLocal'),
]
