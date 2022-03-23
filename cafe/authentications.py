from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
import jwt
from django_prj.settings import get_secret


def get_token(user):
    user_id = user.id
    # 토큰에 담을 유저 정보 -> 기밀 사항은 담으면 안됨
    payload = {
        "user_id": user_id,
    }
    # 토큰 생성, 장고 프로젝트의 시크릿키로 암호화.
    token = jwt.encode(payload, get_secret('secret_key'), 'HS256')
    return {
        "access_token": token,
    }


# request가 들어올 경우 view에 들어가기 전에 실행된다.
# 이것을 통해 현재 로그인 된 사용자를 불러올 수 있음. -> DEFAULT AUTHENTICATION CLASS로 지정해줘야 함.
# DEFAULT AUTHENTICATION CLASS == middleware custom
# 현재 유저가 누구인지 확인하는 단계라고 할 수 있다.
# Custom Authentication
class UserAuthentication(authentication.BaseAuthentication):  # -> 토큰이 있는지 없는지 확인하는 함수
    def authenticate(self, request):
        data = request.META.get('HTTP_AUTHORIZATION')
        # data = request.headers['Authorization']

        # 이게 없으면 처음에 로그인 할 때 토근이 유효하지 않다고 해서 안넘어감!!
        if not data:
            return None  # -> request.user = None
        # token이 있는 경우에만 실행됨
        decoded_token = jwt.decode(data, get_secret('secret_key'), 'HS256')

        user_id = decoded_token.get('user_id', None)  # user id 가 없으면 None return
        # 어차피 None을 반환하니까 에러처리 해줄 필요 없을 것 같음!
        # 위의 코드가 try문 안으로 들어가게 하려면 위의 코드가 발생하는 에러에 대해서도 except 처리 해줘야 함.
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No Such user')

        return (user, None) # -> request.user = user

# authentication_credentials -> 복호화된 토큰의 정보로 인증하는 함수

