from sqlmodel import SQLModel, create_engine
import models

URL_MYSQL = "mysql+pymysql://root:admin_fernando@localhost:3306/fernando_responde"

engine = create_engine(URL_MYSQL, echo=True)