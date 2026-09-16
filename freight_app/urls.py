from django.urls import path
from freight_app.views import (
    CustomTokenObtainPairView, GetUserInformationView, GetTableDataView,
    CarrierDataView, CarriersDataListView, GeneralContactUsView, JustContactUsView,
    ContactDataListView, ToggleStatusView, DeleteCarrierView, DeleteContactFormView,
    DeleteContactView, SiteSettingsView, MCNumberView, MCLookupView
)

urlpatterns = [
    path('sign-in', CustomTokenObtainPairView.as_view(), name='sign_in'),
    path('get-user-information', GetUserInformationView.as_view(), name='get_user_info'),
    path('get-table-data', GetTableDataView.as_view(), name='get_table_data'),
    
    path('CarrierData', CarrierDataView.as_view(), name='carrier_data'),
    path('carriersData', CarriersDataListView.as_view(), name='carriers_list'),
    
    path('general-contact-us', GeneralContactUsView.as_view(), name='general_contact'),
    path('justcontactus', JustContactUsView.as_view(), name='just_contact'),
    path('ContactData', ContactDataListView.as_view(), name='contact_list'),
    
    path('toggleStatus/<int:pk>', ToggleStatusView.as_view(), name='toggle_status'),
    path('deleteCarrier/<int:pk>', DeleteCarrierView.as_view(), name='delete_carrier'),
    path('deleteContactForm/<int:pk>', DeleteContactFormView.as_view(), name='delete_contact_form'),
    path('deleteContact/<int:pk>', DeleteContactView.as_view(), name='delete_contact'),
    
    path('site-settings', SiteSettingsView.as_view(), name='site_settings'),
    
    path('MCnumber/<str:mc>', MCNumberView.as_view(), name='mc_number'),
    path('mc-lookup/<str:mcNumber>', MCLookupView.as_view(), name='mc_lookup'),
]
