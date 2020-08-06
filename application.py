import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from functools import wraps
import random


# Configure application
app = Flask(__name__)

#app.jinja_env.filters["speech_recognition"] = speech_recognition

elim = [0] * 10

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("postgres://xiegxfawoahlfz:f18643c18a8d7be4e604cfc952881518d8095119ba46310befe6009eef79101c@ec2-34-193-232-231.compute-1.amazonaws.com:5432/defhlg16sllii3")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    #db.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS world (user NOT NULL, score NUMERIC NOT NULL)")
    return render_template("index.html")

    
@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        db.execute("CREATE TABLE IF NOT EXISTS scores (idu INTEGER NOT NULL, game_id INTEGER NOT NULL, score NUMERIC NOT NULL, date DATE NOT NULL)")

        # Redirect user to home page
        return render_template("start.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        number_pass = 0
        uppercase = 0
        lowercase = 0

        if request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords don´t match")
            return redirect("/register")
            
        if len(request.form.get("password")) < 8:
            flash("Password must be at least 8 characters long.")
            return redirect("/register")
            
        for ijj in range(len(request.form.get("password"))):
            if str(request.form.get("password"))[ijj] >= '0' and str(request.form.get("password"))[ijj] <= '9':
                number_pass += 1
            elif str(request.form.get("password"))[ijj] >= 'A' and str(request.form.get("password"))[ijj] <= 'Z':
                uppercase += 1
            elif str(request.form.get("password"))[ijj] >= 'a' and str(request.form.get("password"))[ijj] <= 'z':
                lowercase += 1
        if number_pass < 1 or uppercase < 1 or lowercase < 1:
            flash("Password must have at least one lowercase letter, one uppercase letter and one numerical digit.")
            return redirect("/register")
            

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) == 1:
            flash("Taken username")
            return redirect("/register")
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username = request.form.get("username"), hash = generate_password_hash(request.form.get("password")))
            return render_template("login.html")
    else:
        return render_template("register.html")
        
@app.route("/start", methods=["GET", "POST"])
@login_required
def start():
    global digits
    global num
    global p
    global f
    global posible 
    global machinenum
    global counterfordef
    global notdefinite
    global comprobation
    global posibles_left
    global comp
    global discardy
    global councher
    global posible
    global discarded_counter
    global probable
    global discarded
    global history
    global results
    global definite
    global counter
    global loopy
    global validation_counter
    global posibles_left
    global last_posible
    global county
    global definite_confirmation
    global counterfordef
    global comp
    global prove
    global counter_num
    global piquillas
    global fijillas
    global proposed_number
    global machinewin
    global userwin
    global score
    global elim
    global ones
    global tenths
    
    if request.method == "GET":
        return render_template("start.html")
    else:
        num = int(request.form.get("user_number"))
        
        if str(num)[0] == str(num)[1]:
            flash("Do not repeat digits")
            return redirect("/start")
            
        digits = 2
        
        while True:
            approve = 0
            machinenum = random.randint(10 ** (digits - 1), (10 ** digits) - 1)
            if str(machinenum)[0] == str(machinenum)[1]:
                    approve = 1
            if approve == 0:
                break
    
        posible = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        history = []
        results = []
        definite = [None, None]
        probable = [None, None]
        discarded = [None, None]
        counter = 0
        machinewin = 0
        userwin = 0
        p = 0
        f = 0
        discarded_counter = 0
        loopy = 0
        validation_counter = 0
        posibles_left = 0
        last_posible = 0
        county = 0
        definite_confirmation = 0
        counterfordef = 0
        comp = 0
        prove = 0
        piquillas = 0
        fijillas = 0
        score = 0
        elim = [0] * 10
        ones = '_'
        tenths = '_'
    
        db.execute("CREATE TABLE IF NOT EXISTS game (idh INTEGER NOT NULL, proposed_number INTEGER NOT NULL, piquillas NUMERIC NOT NULL, fijillas NUMERIC NOT NULL)")
        define_loopy()
        db.execute("DELETE FROM game")
        return render_template("game.html", ones = ones, tenths = tenths, elim = elim, num = num, machinenum = machinenum, loopy = loopy, piquillas = piquillas, fijillas = fijillas)
        
@app.route("/game", methods=["GET", "POST"])
@login_required
def game():
    global digits
    global num
    global p
    global f
    global posible 
    global machinenum
    global counterfordef
    global notdefinite
    global comprobation
    global posibles_left
    global comp
    global discardy
    global councher
    global posible
    global discarded_counter
    global probable
    global discarded
    global history
    global results
    global definite
    global counter
    global loopy
    global validation_counter
    global posibles_left
    global last_posible
    global county
    global definite_confirmation
    global counterfordef
    global comp
    global prove
    global piquillas
    global fijillas
    global proposed_number
    global machinewin
    global userwin
    global score
    global elim
    global game_id
    global ones
    global tenths
    
    if request.method == "GET":
    
        return render_template("game.html", elim = elim, num = num, machinenum = machinenum, loopy = loopy, piquillas = piquillas, fijillas = fijillas)
    else:
        
        p = int(request.form.get("picas"))
        f = int(request.form.get("fijas"))
        elim1 = request.form.get("elim1")
        elim2 = request.form.get("elim2")
        
        
        if elim1 != '':
            elim1 = int(elim1)
            elim[elim1] = 1
        if elim2 != '':
            elim2 = int(elim2)
            elim[elim2] = 1
            
        if ones != '' and ones != '_':
            ones = ones
        else:
            ones = request.form.get("ones")
            if ones != '':
                ones = int(request.form.get("ones"))
            else: 
                ones = '_'
        if tenths != '' and tenths != '_':
            tenths = tenths
        else:
            tenths = request.form.get("tenths")
            if tenths != '':
                tenths = int(request.form.get("tenths"))
            else: 
                tenths = '_'
        
        proposed_number = int(request.form.get("proposition"))
        
        if str(proposed_number)[0] == str(proposed_number)[1]:
            flash("Do not repeat digits of the proposed number")
            rows = db.execute("SELECT proposed_number, piquillas, fijillas FROM game WHERE idh = :idh", idh = session["user_id"])
            return render_template("game.html", ones = ones, tenths = tenths, elim = elim, rows = rows, score = score, machinenum = machinenum, loopy = loopy, proposed_number = proposed_number, num = num, piquillas = piquillas, fijillas = fijillas)
 
        if counter == 1:
            randomgif = random.randint(0, 3)
            if machinewin == 1:
                if score == 0:
                    score = 1.5
                score = 1.5 * score
            numrows = db.execute("SELECT COUNT(*) FROM scores WHERE idu = :idu", idu = session["user_id"])
            if numrows == [{'COUNT(*)': 0}]:
                game_id = 1
            else:
                game_id = numrows[0]
                game_id = game_id["COUNT(*)"]
                game_id += 1
            db.execute("INSERT INTO scores (idu, game_id, score, date) VALUES(:idu, :game_id, :score, :date)", idu = session["user_id"], game_id = game_id, score = score, date = datetime.datetime.now())
            rows = db.execute("SELECT game_id, score, date FROM scores WHERE idu = :idu ORDER BY game_id DESC", idu = session["user_id"])
            return render_template("table.html", numrows = numrows, game_id = game_id, rows = rows, randomgif = randomgif, machinewin = machinewin, userwin = userwin, num = num, machinenum = machinenum)
        
           
        process_answer()
        if counter == 1:
            randomgif = random.randint(0, 3)
            if machinewin == 1:
                if score == 0:
                    score = 1.5
                score = 1.5 * score
            numrows = db.execute("SELECT COUNT(*) FROM scores WHERE idu = :idu", idu = session["user_id"])
            if numrows == [{'COUNT(*)': 0}]:
                game_id = 1
            else:
                game_id = numrows[0]
                game_id = game_id["COUNT(*)"]
                game_id += 1
            db.execute("INSERT INTO scores (idu, game_id, score, date) VALUES(:idu, :game_id, :score, :date)", idu = session["user_id"], game_id = game_id, score = score, date = datetime.datetime.now())
            rows = db.execute("SELECT game_id, score, date FROM scores WHERE idu = :idu ORDER BY game_id DESC", idu = session["user_id"])
            return render_template("table.html", numrows = numrows, game_id = game_id, rows = rows, randomgif = randomgif, machinewin = machinewin, userwin = userwin, num = num, machinenum = machinenum)
        
       
        define_loopy()
        if counter == 1:
            randomgif = random.randint(0, 3)
            if machinewin == 1:
                if score == 0:
                    score = 1.5
                score = 1.5 * score
            numrows = db.execute("SELECT COUNT(*) FROM scores WHERE idu = :idu", idu = session["user_id"])
            if numrows == [{'COUNT(*)': 0}]:
                game_id = 1
            else:
                game_id = numrows[0]
                game_id = game_id["COUNT(*)"]
                game_id += 1
            db.execute("INSERT INTO scores (idu, game_id, score, date) VALUES(:idu, :game_id, :score, :date)", idu = session["user_id"], game_id = game_id, score = score, date = datetime.datetime.now())
            rows = db.execute("SELECT game_id, score, date FROM scores WHERE idu = :idu ORDER BY game_id DESC", idu = session["user_id"])
            return render_template("table.html", numrows = numrows, game_id = game_id, rows = rows, randomgif = randomgif, machinewin = machinewin, userwin = userwin, num = num, machinenum = machinenum)
        score += 1  
        db.execute("INSERT INTO game (idh, proposed_number, piquillas, fijillas) VALUES (:idh, :proposed_number, :piquillas, :fijillas)", idh = session["user_id"], proposed_number = proposed_number, piquillas = piquillas, fijillas = fijillas) 
        rows = db.execute("SELECT proposed_number, piquillas, fijillas FROM game WHERE idh = :idh", idh = session["user_id"])
        
        return render_template("game.html", ones = ones, tenths = tenths, elim = elim, rows = rows, score = score, machinenum = machinenum, loopy = loopy, proposed_number = proposed_number, num = num, piquillas = piquillas, fijillas = fijillas)
    

@app.route("/table")
@login_required
def table():
    global randomgif
    global machinewin
    global userwin
    global num
    global machinenum
    global game_id
    numrows = db.execute("SELECT COUNT(*) FROM scores WHERE idu = :idu", idu = session["user_id"])
    print(numrows)
    rows = db.execute("SELECT game_id, score, date FROM scores WHERE idu = :idu ORDER BY game_id DESC", idu = session["user_id"])
    if numrows != [{'COUNT(*)': 0}]:
        dict = numrows[0]
        game_id = int(dict["COUNT(*)"])
        return render_template("table.html", numrows = numrows, rows = rows, game_id = game_id)
    else:
        flash("Play in order to see your score!")
        return render_template("table.html", numrows = numrows, rows = rows)
    
@app.route("/ranking")
def ranking():
    global rank
    rank = 0
    rows = db.execute("SELECT user, score FROM world ORDER BY score ASC")
    return render_template("ranking.html", rank = rank, rows = rows)
    
@app.route("/appearw")
@login_required
def appearw():
    global game_id
    appear()
    return redirect("/ranking")
    

def define_loopy():

    global counterfordef
    global notdefinite
    global comprobation
    global posibles_left
    global comp
    global discardy
    global councher
    global posible
    global discarded_counter
    global probable
    global discarded
    global history
    global results
    global definite
    global counter
    global loopy
    global validation_counter
    global posibles_left
    global last_posible
    global machinewin
    global userwin
    
    counterfordef = 0
    notdefinite = 0
    posibles_left = 0
    comp = 0
    councher = 0
    comprobation = 1
    discardy = []
    
    if comp == 0:
        #eliminating possible cases of false definites
        if definite[0] != None or definite[1] != None:
            comp = 1
            for j in range(2):
                for i in range(len(discarded)):
                    if definite[j] != None and definite[j] == discarded[i]:
                        definite[j] = None
                        if j == 0:
                            definite[1] = int(str(history[len(history) - 2])[1])
                        else:
                            definite[0] = int(str(history[len(history) - 2])[0])
    if validation_counter != 2:
        if len(discarded) > 2 or discarded[0] != None:
            while True:
                approve = 0
                randomn = random.randint(10 ** (digits - 1), (10 ** digits) - 1)
                for i in range(len(discarded)):
                    if str(randomn)[0] == str(discarded[i]) or str(randomn)[1] == str(discarded[i]) or str(randomn)[0] == str(randomn)[1]:
                        approve = 1
                if approve == 0:
                    break
        else:
            while True:
                approve = 0
                randomn = random.randint(10 ** (digits - 1), (10 ** digits) - 1)
                if str(randomn)[0] == str(randomn)[1]:
                    approve = 1
                if approve == 0:
                    break
        loopy = randomn
        #setting definite/probable/random number to loopy    
        
        for u in range(len(discarded)):
            if probable[0] == discarded[u] or probable[1] == discarded[u]:
                comprobation += 1
                
        if probable[0] == None and probable[1] == None:
            loopy = randomn
            
        else:
            if comprobation == 1 or prove == 1:
                if probable[0] == int(str(history[len(history) - 2])[0]) and probable[1] == int(str(history[len(history) - 2])[1]):
                    probable[1] = int(str(history[len(history) - 2])[0])
                    while True:
                        approve = 0
                        randoml = random.randint(1, 9)
                        for i in range(len(discarded)):
                            if randoml == discarded[i] or randoml == probable[1]:
                                approve = 1
                        if approve == 0:
                            break
                    probable[0] = randoml
                    probablee = (probable[0] * 10) + probable[1]
                    loopy = probablee
                    
                else:
                    if str(probable)[0] == str(history[len(history) - 1])[0] and str(probable)[1] == str(history[len(history) - 1])[1]:
                        probable[0] = int(str(history[len(history) - 1])[1])
                        probable[1] = int(str(history[len(history) - 1])[0])
                    probables = (probable[0] * 10) + probable[1]
                    loopy = probables
            elif comprobation > 1:
                while True:
                    approve = 0
                    randomr = random.randint(10 ** (digits - 1), (10 ** digits) - 1)
                    for i in range(len(discarded)):
                        if str(randomr)[0] == str(discarded[i]) or str(randomr)[1] == str(discarded[i]) or str(randomr)[0] == str(randomr)[1]:
                            approve = 1
                    if approve == 0:
                        break
                
        for i in range(2):
            if definite[i] != None:
                if i == 0:
                    loopynum = int(str(loopy)[1])
                    if loopynum == definite[i]:
                        if loopy == history[len(history) - 1] or probable[1] == None or int(str(loopy)[1]) == definite[0] or probable[1] == definite[0]:
                            while True:
                                approve = 0
                                loopynum = random.randint(1, 9)
                                for z in range(len(discarded)):
                                    if loopynum == int(str(history[len(history) - 1])[1]) or loopynum == discarded[z] or loopynum == definite[0]:
                                        approve = 1
                                if approve == 0:
                                    break
                        else:
                            loopynum = probable[1]
                    loopy = loopynum + (10 * definite[i])
                else:
                    loopynum = int(str(loopy)[0])
                    if loopynum == definite[i]:
                        if loopy == history[len(history) - 1] or probable[0] == None or probable[0] == 0 or probable[0] == definite[1]:
                            while True:
                                approve = 0
                                loopynum = random.randint(1, 9)
                                for w in range(len(discarded)):
                                    if loopynum == int(str(history[len(history) - 1])[0]) or loopynum == discarded[w] or loopynum == definite[1]:
                                        approve = 1
                                if approve == 0:
                                    break
                        else:
                            loopynum == probable[0]
                    loopy = (10 * loopynum) + definite[i]
     
    if validation_counter == 2:
        if definite[0] != None and definite[1] != None:
            loopy = (definite[0] * 10) + definite[1]
        else:
            for y in range(len(posible)):
                if posible[y] != None:
                    posibles_left += 1
                    if posible[y] != definite[0] and posible[y] != definite[1]:
                        last_posible = posible[y]
            if posibles_left == 2:
                if definite[0] != None:
                    definite[1] = last_posible
                else:
                    definite[0] = last_posible
                loopy = (definite[0] * 10) + definite[1]
            else:
                for h in range(len(posible)):
                    if posible[h] != None:
                        discardy.append(posible[h])
                if len(discardy) > 4:
                    while True:
                        approve = 0
                        randomq = random.randint(10 ** (digits - 1), (10 ** digits) - 1)
                        for i in range(len(discarded)):
                            if (int(str(randomq)[0]) == discarded[i] or int(str(randomq)[1]) == discarded[i]
                                or str(randomq)[0] == str(randomq)[1] or int(str(randomq)[0]) == definite[1]
                                or int(str(randomq)[1]) == definite[0]  or int(str(randomq)[0]) == definite[0]
                                or int(str(randomq)[1]) == definite[1]):
                                approve = 1
                        if approve == 0:
                            break
                    loopy = randomq
                else:
                    while True:
                        approve = 0
                        ran1 = random.randint(0, len(discardy) - 1)
                        if discardy[ran1] == definite[1] or discardy[ran1] == definite[0] or discardy[ran1] == 0:
                            approve = 1
                        if approve == 0:
                            break
                    while True:
                        approve = 0
                        ran2 = random.randint(0, len(discardy) - 1)
                        if ran1 == ran2 or discardy[ran2] == definite[1] or discardy[ran2] == definite[0]:
                            approve = 1
                        if approve == 0:
                            break
                    loopy = (discardy[ran1] * 10) + discardy[ran2]
            
    
    if loopy == num:
            counter = 1
            machinewin = 1
            
def process_answer():
    global digits
    global num
    global p
    global f
    global posible 
    global machinenum
    global counterfordef
    global notdefinite
    global comprobation
    global posibles_left
    global comp
    global discardy
    global councher
    global posible
    global discarded_counter
    global probable
    global discarded
    global history
    global results
    global definite
    global counter
    global loopy
    global validation_counter
    global posibles_left
    global last_posible
    global county
    global definite_confirmation
    global counterfordef
    global comp
    global prove
    global piquillas
    global fijillas
    global proposed_number
    global machinewin
    global userwin
    
    history.append(loopy) 
    results.append(p+f)
    
    for sa in range(len(history)):
        if history[sa] == 0:
            history.remove(history[sa])
                    
    if p + f == 0:
        if len(history) > 1 and str(loopy)[0] == str(history[len(history) - 2])[1]:
            definite[1] = int(str(history[len(history) - 2])[0])
            counterfordef += 1
        if len(history) > 1 and int(str(loopy)[0]) == int(str(history[len(history) - 2])[0]) and definite[0] != None:
            definite[1] = int(str(history[len(history) - 2])[1])
            definite[0] = None
            discarded.append(definite[0])
            posible[int(str(loopy)[0])] = None
            counterfordef += 1
            
        if str(loopy)[1] == str(posible[int(str(loopy)[1])]):
            discarded_counter += 2
        else:
            discarded_counter += 1
            #definite[1] = int(str(history[len(history) - 2])[1])
        for j in range(len(str(loopy))):
            for o in range(len(discarded)):
                if discarded_counter > 2 and discarded[o] != int(str(loopy)[j]):
                    county += 1
                    if county == len(discarded):
                        discarded.append(int(str(loopy)[j]))
                        posible[int(str(loopy)[j])] = None
                #give a number to first 2 elements in discarded list
                if j == 0 and discarded_counter < 3:
                    discarded[0] = int(str(loopy)[j])
                    posible[int(str(loopy)[j])] = None
                if j == 1 and discarded_counter < 3:
                    discarded[1] = int(str(loopy)[j])
                    posible[int(str(loopy)[j])] = None
            county = 0
            
    if validation_counter != 2:        
        if p == 2:
            probable[0] = int(str(loopy)[1])
            probable[1] = int(str(loopy)[0])
        
        else:
            if f == 1:
                if str(loopy)[0] == str(definite[0]):
                    discarded.append(int(str(loopy)[1]))
                    posible[int(str(loopy)[1])] = None
                    
                elif str(loopy)[1] == str(definite[1]):
                    discarded.append(int(str(loopy)[0]))
                    posible[int(str(loopy)[0])] = None
                    notdefinite = 1
                
                #try to prove that number is definite with discarded num        
                elif int(str(loopy)[0]) == posible[int(str(loopy)[0])] and int(str(loopy)[0]) != definite[0]:
                    if discarded[0] != None:
                        if discarded[0] == int(str(loopy)[1]):
                            if len(discarded) > 1:
                                probable[0] = int(str(loopy)[0])
                                probable[1] = discarded[0]
                            else:
                                while True:
                                    approve = 0
                                    randoms = random.randint(0, 9)
                                    for i in range(len(discarded)):
                                        if randoms == discarded[i] or randoms == int(str(loopy)[1]) or randoms == int(str(loopy)[0]):
                                            approve = 1
                                    if approve == 0:
                                        break
                                probable[1] = randoms
                        else:
                            #loopy = loopy - int(str(loopy)[1]) + discarded[0]
                            probable[0] = int(str(loopy)[0])
                            probable[1] = discarded[0]
                    else:
                        probable[0] = int(str(loopy)[0])
                        while True:
                            approve = 0
                            randoms = random.randint(0, 9)
                            for x in range(len(discarded)):
                                if randoms == discarded[x] or randoms == int(str(loopy)[1]) or randoms == int(str(loopy)[0]):
                                    approve = 1
                            if approve == 0:
                                break
                        probable[1] = randoms
                if len(history) > 1:
                    if str(loopy)[0] == str(history[len(history) - 2])[1]:
                        definite[0] = int(str(loopy)[0])
                    if str(loopy)[1] == str(history[len(history) - 2])[0]:
                        definite[1] = int(str(loopy)[1])
                    else:
                        if notdefinite == 0:
                            definite[0] = int(str(loopy)[0])
            if p == 1:
                if definite[0] == int(str(loopy)[0]):
                    definite[0] = int(str(loopy)[1])
                if len(history) > 1:
                    if str(loopy)[0] == str(history[len(history) - 2])[0] and results[len(results) - 2] == 1:
                        if str(history[len(history) - 2])[1] == str(discarded[len(discarded) - 1]):
                            posible[int(str(history[len(history) - 2])[1])] = int(str(history[len(history) - 2])[1])
                            discarded.remove(int(str(history[len(history) - 2])[1]))
                            definite[1] = int(str(history[len(history) - 2])[1])
                            discarded.append(int(str(loopy)[0]))
                            posible[int(str(loopy)[0])] = None
                            definite[0] = int(str(loopy)[1])
                        else:
                            definite[0] = int(str(loopy)[1])
                            definite[1] = int(str(history[len(history) - 2])[1])
                    
                if definite[0] != None and definite[1] == None:
                    definite[1] = int(str(loopy)[0])
                    if definite[1] == definite[0]:
                        definite[0] = None
                if definite[1] != None and definite[0] == None:
                    definite[0] = int(str(loopy)[1])
                    if definite[1] == definite[0]:
                        definite[1] = None
                if str(loopy)[1] == '0':
                    definite[1] == int(str(loopy)[0])
                    discarded.append(int(str(loopy)[1]))
                    posible[int(str(loopy)[1])] = None
                    counterfordef += 1
                else:
                    probable[0] = int(str(loopy)[1])
                    prove += 1
                    if discarded[0] != None:
                        probable[1] = discarded[0]
                    else:
                        while True:
                            approve = 0
                            randoms = random.randint(0, 9)
                            for q in range(len(discarded)):
                                if randoms == discarded[q] or randoms == int(str(loopy)[1]) or randoms == probable[0]:
                                    approve = 1
                            if approve == 0:
                                break
                        probable[1] = randoms
                        
        if definite[0] != None or definite[1] != None:
            for ca in range(len(results)):
                if results[ca] == 1 and str(history[ca])[0] != str(definite[0]) and str(history[ca])[1] != str(definite[0]) and str(history[ca])[0] != str(definite[1]) and str(history[ca])[1] != str(definite[1]): 
                    for foo in range(2):
                        if int(str(history[ca])[foo]) == posible[int(str(history[ca])[foo])]:
                            councher += 1
                            counchers = int(str(history[ca])[foo])
                        if councher == 1:
                            if definite[0] != None:
                                definite[1] = int(str(history[ca])[foo])
                            else:
                                definite[0] = int(str(history[ca])[foo])
   
    if definite[0] != None or definite[1] != None:
        for a in range(len(history)):
            for z in range(2):
                if definite[z] == int(str(history[a])[0]) or definite[z] == int(str(history[a])[1]):
                    if results[a] == 1:
                        counterfordef += 1
        if counterfordef > 1:
            definite_confirmation = 1
            u = 0
            while u < len(discarded):
                if discarded[u] != None:
                    if discarded[u] == definite[0] or discarded[u] == definite[1]:
                        posible[int(discarded[u])] = discarded[u]
                        discarded.remove(discarded[u])
                        #u = 0
                u += 1
                
     #discarding other numbers that accompanied definite and should be discarded   
    if validation_counter == 0:
        for h in range(len(history)):
            for r in range(2):
                if definite[r] != None and str(results[h]) == '1' and definite_confirmation == 1:
                    if str(history[h])[1] == str(definite[r]) or str(history[h])[0] == str(definite[r]):
                        if str(history[h])[0] == str(definite[r]):
                            discarded.append(int(str(history[h])[1]))
                            posible[int(str(history[h])[1])] = None
                        if str(history[h])[1] == str(definite[r]):
                            discarded.append(int(str(history[h])[0]))
                            posible[int(str(history[h])[0])] = None
                        validation_counter = 1
                    
                
    #search by 2O after 1 definite
    if validation_counter == 2:
        if p == 1:
            if definite[0] != None:
                definite[1] = int(str(loopy)[0])
                discarded.append(int(str(loopy)[1]))
                posible[int(str(loopy)[1])] = None
            elif definite[1] != None:
                definite[0] = int(str(loopy)[1])
                discarded.append(int(str(loopy)[0]))
                posible[int(str(loopy)[0])] = None
        if f == 1:
            if definite[0] != None:
                definite[1] = int(str(loopy)[1])
                discarded.append(int(str(loopy)[0]))
                posible[int(str(loopy)[0])] = None
            elif definite[1] != None:
                definite[0] = int(str(loopy)[0])
                discarded.append(int(str(loopy)[1]))
                posible[int(str(loopy)[1])] = None 
    p = 0
    f = 0
    if validation_counter == 1:
        validation_counter = 2
    #give info to user about my num
    fijillas = 0
    piquillas = 0

    for l in range(2):
        if str(proposed_number)[l] == str(machinenum)[l]:
            fijillas += 1
    if str(proposed_number)[0] == str(machinenum)[l]:
        piquillas += 1
    if str(proposed_number)[l] == str(machinenum)[0]:
        piquillas += 1
            
    
    if fijillas == 2:
        counter += 1
        userwin = 1
        
def appear():
    global game_id
    final_score = 0
    for ij in range(3):
        numcount = game_id - ij
        row = db.execute("SELECT score FROM scores WHERE game_id = :numcount AND idu = :idu", numcount = numcount, idu = session["user_id"]) 
        dicty = row[0]
        final_score += dicty["score"]
    final_score /= 3
    final_score = str(round(final_score, 2))
    user = db.execute("SELECT username FROM users WHERE id = :id", id = session["user_id"])
    user = user[0]
    user = user["username"]
    if game_id > 3:
        db.execute("UPDATE world SET score = :score WHERE user = :user", score = final_score, user = user)
    else:
        db.execute("INSERT INTO world (user, score) VALUES (:user, :score)", user = user, score = final_score)
    return redirect("/ranking")
    
def rankp(rank):
    rank += 1
    return rank

app.jinja_env.globals.update(appear=appear)
app.jinja_env.globals.update(rankp=rankp)