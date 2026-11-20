from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, upload_views

router = DefaultRouter()
router.register(r'programs', views.ProgramViewSet, basename='program')
router.register(r'curriculum-subjects', views.CurriculumSubjectViewSet, basename='curriculum-subject')
router.register(r'applications', views.ApplicationViewSet, basename='application')
router.register(r'work-experiences', views.WorkExperienceViewSet, basename='work-experience')
router.register(r'documents', views.ApplicantDocumentViewSet, basename='document')
router.register(r'tor-documents', views.TORDocumentViewSet, basename='tor-document')
router.register(r'subject-matches', views.SubjectMatchViewSet, basename='subject-match')
router.register(r'chat-conversations', views.ChatConversationViewSet, basename='chat-conversation')

urlpatterns = [
    path('', views.health_check, name='health-check'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/google/', views.google_auth, name='google-auth'),
    path('auth/me/', views.me, name='me'),
    path('auth/profile/', views.me, name='profile'),
    path('auth/change-password/', views.change_password, name='change-password'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('upload/document/', upload_views.upload_document, name='upload-document'),
    path('documents/<uuid:document_id>/preview/', upload_views.preview_document, name='preview-document'),
    path('upload/curriculum/', upload_views.upload_curriculum, name='upload-curriculum'),
    path('work-experience/add/', upload_views.add_work_experience, name='add-work-experience'),
    path('application/process/', upload_views.process_application, name='process-application'),
    path('recommend-course/', upload_views.recommend_course, name='recommend-course'),
    path('predictions/', upload_views.get_predictions, name='get-predictions'),
    path('chat/message/', upload_views.chat_message, name='chat-message'),
    path('applications/<uuid:application_id>/certificate-valuation/', upload_views.get_certificate_valuation, name='certificate-valuation'),
    path('applications/<uuid:application_id>/certificate-valuation/audit/', upload_views.save_certificate_audit_decision, name='certificate-audit'),
    path('certificate-review/uat-feedback/', upload_views.record_uat_feedback, name='certificate-uat-feedback'),
    path('', include(router.urls)),
]
