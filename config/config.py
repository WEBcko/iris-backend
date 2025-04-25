import os
from dotenv import load_dotenv
from datetime import timedelta

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "posgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "blogdb")
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}';

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secreto")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1) # Define o tempo de vida do token de acesso (minutos)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30) # Define o tempo de vida do token de refresh (dias)
