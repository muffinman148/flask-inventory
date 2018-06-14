import os

# Makes .env config
def makeEnv():
    envConfig = []
    valid = False

    while not valid:
        secretkey = input("Define the SECRET_KEY= ")
        if secretkey:
            break

    while not valid:
        sqlalchemy_db = input("Define the SQLALCHEMY_DATABASE_URI= ")
        if sqlalchemy_db:
            break

    while not valid:
        admins = input("Define the ADMINS(Admin's Email)= ")
        if "@" in admins:
            break

    envConfig.append("SECRET_KEY = os.environ.get('SECRET_KEY') or '" + secretkey + "'")
    envConfig.append("SQLALCHEMY_DATABASE_URI = '" + sqlalchemy_db + "'")
    envConfig.append("ADMINS = ['" + admins + "']")

    return envConfig

# Makes .flaskenv config
def makeFlaskEnv():
    flaskConfig = []
    valid = False

    while not valid:
        flaskapp = input("Define the FLASK_APP= ")
        if ".py" in flaskapp:
            break
        else:
            print("Invalid FLASK_APP name. Try .py file.\n")

    while not valid:
        flaskenv = input("Production or Development? ")
        if flaskenv.lower() in ("production", "p", "prod"):
            flaskenv = "production"
            break
        elif flaskenv.lower() in ("development", "d", "dev"):
            flaskenv = "development"
            break
        else:
            print("Invalid input. Try 'prod' for production or 'dev' for development.\n")

    flaskConfig.append("FLASK_APP=" + flaskapp)
    flaskConfig.append("FLASK_ENV=" + flaskenv)

    return flaskConfig

def main():
    #--------# .env File #
    
    # Initialize Values
    envFile = ".env"
    env = makeEnv()

    # Saves old file
    if os.path.exists(envFile):
        os.replace(envFile, ".env.bak")
    
    # Creates File
    newEnvFile = open(envFile, "w")
    for x in range(0, len(env)):
        newEnvFile.write(env[x] + "\n")
    newEnvFile.close()
    
    #--------# .flaskenv File #

    # Initialize Values
    flaskFile = ".flaskenv"
    flask = makeFlaskEnv()

    # Saves old file
    if os.path.exists(flaskFile):
        os.replace(flaskFile, ".flaskenv.bak")

    # Creates File
    newFlaskFile = open(flaskFile, "w")
    for x in range(0, len(flask)):
        newFlaskFile.write(flask[x] + "\n")
    newFlaskFile.close()

if __name__ == "__main__":
    main()
