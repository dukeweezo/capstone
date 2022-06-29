import os

#CAPSTONE_URL = os.environ.get("CAPSTONE_URL")
#CAPSTONE_APIKEY = os.environ.get("CAPSTONE_APIKEY")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
MEDIA_URL = '/media/'