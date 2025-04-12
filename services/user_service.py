import os
from werkzeug.utils import secure_filename
from repositories.comment_repository import CommentRepository
from repositories.user_repository import UserRepository
from utils.file_utils import allowed_file, generate_filename
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from utils.file_utils import  SERVER_IP

UPLOAD_FOLDER = "uploads/profile_pictures"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "mp4", "avi", "mov", "mkv", "webm", "flv", "wmv"}


class UserService:
    @staticmethod
    def save_profile_image(user_id, image):
        """ Salva a imagem no servidor e atualiza o perfil do usuário """
        if image and allowed_file(image.filename):
            filename = generate_filename(user_id, image.filename)  # 🔹 Gera nome único
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            image.save(filepath)  # 🔹 Salva a imagem no diretório
            image_url = f"/uploads/profile_pictures/{filename}"

            updated_user = UserRepository.update_profile_image(user_id, filename)
            return updated_user, image_url

        return None, None

    @staticmethod
    def toggle_favorite(user_id, post_id):
        user = UserRepository.get_user_by_id(user_id)
        post = UserRepository.get_post_by_id(post_id)

        if not user or not post:
            return {"error": "User or Post not find"}, 400
        
        if post in user.favorites:
            UserRepository.remove_favorite(user, post)
            return {"message": "Post remove from favorite. "}, 200
        
        UserRepository.add_favorite(user, post)
        
        return {"message": "Post added to favorite"}, 200
    
    @staticmethod
    def toggle_like(user_id, comment_id):
        user = UserRepository.get_user_by_id(user_id)
        comment = UserRepository.get_comment_by_id(comment_id)

        if not user or not comment:
            return {"error": "User or comment not find"}, 400
        
        if comment in user.likes:
            UserRepository.remove_like(user, comment)
            return {"message": "Like Removed. "}, 200
        
        UserRepository.add_like(user, comment)
        
        return {"message": "Like Added"}, 200
    
    @staticmethod
    def list_favorites(user_id):

        user = UserRepository.get_user_by_id(user_id)

        if not user:
            return {"error": "User not find"}, 400
       
        favorites = UserRepository.get_favorite_posts_by_user(user)
        
        return [
            {
                "id": fav.id,
                "title": fav.title,
                "description": fav.description,
                "user_id": fav.user_id,
                "author": UserRepository.get_username_by_id(fav.user_id),
                "author_image": f"{request.host_url}{UserRepository.get_user_profile_image(fav.user_id)}" 
                    if UserRepository.get_user_profile_image(fav.user_id) else None,
                "image_url": f"{request.host_url}{fav.image_url}" if fav.image_url else None,
                "favorite_number": fav.favorites_count()
            }
            for fav in favorites
        ], 200

    def toggle_follow(follower_id, followed_id):
        follower = UserRepository.get_user_by_id(follower_id)
        followed = UserRepository.get_user_by_id(followed_id)

        if not followed or not followed:
            return {"error": "Usuário não encontrado"}, 404
        if follower == followed:
            return {"error": "Você não pode seguir a si mesmo"}, 400
        
        if UserRepository.is_following(follower, followed):
            UserRepository.unfollow_user(follower, followed)
            return {"message": f"Você deixou de seguir {followed.username}"}, 200
        else: 
            UserRepository.follow_user(follower, followed)
            return {"message": f"Agora você está seguindo {followed.username}"}, 200

    @staticmethod
    def get_followers(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return {"error": "Usuário não encontrado"}, 404
        
        followers = UserRepository.get_followers(user)
        return {"followers": [follower.username for follower in followers]}, 200

    @staticmethod
    def get_following(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return {"error": "Usuário não encontrado"}, 404
        
        following = UserRepository.get_following(user)  
        return {"following": [followed.username for followed in following]}, 200

    @staticmethod
    def search_users(name):
        users = UserRepository.search_users(name)
        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "user_image": f"{SERVER_IP}/uploads/profile_pictures/{UserRepository.get_user_profile_image(user.id)}",
                "followers_number": user.followers.count()
            }
            for user in users
        ], 200
      
    def get_user_by_id(user_id):

        user = UserRepository.get_user_by_id(user_id)

        if not user:
            return {"error": "Usuário não encontrado"}, 404
        
        is_following = False

        if verify_jwt_in_request() and get_jwt_identity():
            follower = UserRepository.get_user_by_id(get_jwt_identity())
            followed = UserRepository.get_user_by_id(user_id)
            is_following = UserRepository.is_following(follower, followed)
            print(is_following)

        return {
            "user_image": f"{SERVER_IP}/api/user/uploads/profile_pictures/{UserRepository.get_user_profile_image(user_id)}",
            "username": user.username,
            "is_following": is_following,
            "followers_number": user.followers.count(),
            "following_number": user.following.count()
        }, 200
