import sqlite3
from flask import Flask, render_template, request, redirect 

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin_login')
def admin_login():
    return render_template('adminlogin.html')


@app.route('/adashboard', methods=['POST'])
def adashboard():
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    result = request.form
    credentials = []
    for key, value in result.items():
        credentials.append(value)
    cursor.execute('''SELECT ADMIN_USERNAME FROM ADMIN''')
    username = cursor.fetchall()
    arr_username = []
    for i in username:
        arr_username += i
    if credentials[0] in arr_username:
        cursor.execute('''SELECT ADMIN_PASSWORD FROM ADMIN WHERE ADMIN_USERNAME=?''', (str(credentials[0]),))
        password = cursor.fetchone()
        if credentials[1] in str(password):
            user = "http://127.0.0.1:5000/admin_profile" + "/%s" % credentials[0]
            return redirect(user)
        else:
            return render_template("log.html",RES="Wrong Password")
    else:
        return render_template("log.html",RES="Invalid User")


@app.route('/admin_profile/<string:user>')
def admin_profile(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM ADMIN WHERE ADMIN_USERNAME=?''', (user,))
    det = cursor.fetchall()
    details = []
    for i in det:
        details += i
    return render_template('admindashboard.html', USER=user, NAME=details[0],ADMIN_USERNAME=details[1], ADMIN_PASSWORD=details[2])


@app.route('/admin_influencers/<string:user>')
def admin_influencers(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT FIRST_NAME, LAST_NAME, EMAIL_ID, USERNAME, CATEGORY, POSITION, REACH, FLAG FROM INFLUENCER ''')
    result = cursor.fetchall()
    return render_template('admininfluencers.html', RESULT=result, USER=user)


@app.route('/admin_save_influencers/<string:user>', methods=['POST'])
def admin_save_influencers(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    req = request.form
    l=[]
    for key,value in req.items():
        l.append(key)
        l.append(value)
    if l[0]=="flag":
        cursor.execute('''UPDATE INFLUENCER SET FLAG="YES" WHERE USERNAME=?''',(l[1],))
    elif l[0] =="del":
        cursor.execute('''DELETE FROM INFLUENCER WHERE USERNAME=?''',(l[1],))
        cursor.execute('''UPDATE CAMPAIGN_REQUEST SET INFLUENCER_USERNAME="",REQUEST="",REQUEST_PERSON="" WHERE INFLUENCER_USERNAME=?''',(l[1],))
        cursor.execute('''UPDATE CAMPAIGN SET INFLUENCER_USERNAME="",VISIBILITY="PUBLIC" WHERE INFLUENCER_USERNAME=?''',(l[1],))
    elif l[0]=="rflag":
        cursor.execute('''UPDATE INFLUENCER SET FLAG="" WHERE USERNAME=?''',(l[1],))
    conn.commit()
    val = "http://127.0.0.1:5000/admin_influencers/" + "%s" % user
    return redirect(val)


@app.route('/admin_campaigns/<string:user>')
def admin_campaigns(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT CAMPAIGN_NAME,SPONSOR_USERNAME, DESCRIPTION,END_DATE,BUDGET,VISIBILITY,INFLUENCER_USERNAME,FLAG FROM CAMPAIGN''')
    result = cursor.fetchall()
    return render_template('admincampaigns.html', RESULT=result, USER=user)


@app.route('/admin_save_campaigns/<string:user>', methods=['POST'])
def admin_save_campaigns(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    req = request.form
    l=[]
    for key,value in req.items():
        l.append(key)
        l.append(value)
    if l[0]=="flag":
        cursor.execute('''UPDATE CAMPAIGN SET FLAG="YES" WHERE CAMPAIGN_NAME=?''',(l[1],))
    elif l[0] =="del":
        cursor.execute('''DELETE FROM CAMPAIGN WHERE CAMPAIGN_NAME=?''',(l[1],))
        cursor.execute('''DELETE FROM CAMPAIGN_REQUEST WHERE CAMPAIGN_NAME=?''',(l[1],))
    elif l[0]=="rflag":
        cursor.execute('''UPDATE CAMPAIGN SET FLAG="" WHERE CAMPAIGN_NAME=?''',(l[1],))
    conn.commit()
    val = "http://127.0.0.1:5000/admin_campaigns/" + "%s" % user
    return redirect(val)


@app.route('/admin_sponsors/<string:user>')
def admin_sponsors(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT COMPANY_NAME, COMPANY_USERNAME, EMAIL_ID, INDUSTRY, FLAG FROM SPONSOR''')
    result = cursor.fetchall()
    return render_template('adminsponsors.html', RESULT=result, USER=user)


@app.route('/admin_save_sponsors/<string:user>', methods=['POST'])
def admin_save_sponsors(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    req = request.form
    l=[]
    for key,value in req.items():
        l.append(key)
        l.append(value)
    if l[0]=="flag":
        cursor.execute('''UPDATE SPONSOR SET FLAG="YES" WHERE COMPANY_USERNAME=?''',(l[1],))
        cursor.execute('''UPDATE CAMPAIGN SET FLAG="YES" WHERE SPONSOR_USERNAME=?''',(l[1],))
    elif l[0] =="del":
        cursor.execute('''DELETE FROM SPONSOR WHERE COMPANY_USERNAME=?''',(l[1],))
        cursor.execute('''DELETE FROM CAMPAIGN WHERE SPONSOR_USERNAME=?''',(l[1],))
        cursor.execute('''DELETE FROM CAMPAIGN_REQUEST WHERE SPONSOR_USERNAME=?''',(l[1],))
    elif l[0]=="rflag":
        cursor.execute('''UPDATE SPONSOR SET FLAG="" WHERE COMPANY_USERNAME=?''',(l[1],))
        cursor.execute('''UPDATE CAMPAIGN SET FLAG="" WHERE SPONSOR_USERNAME=?''',(l[1],))
    conn.commit()
    val = "http://127.0.0.1:5000/admin_sponsors/" + "%s" % user
    return redirect(val)


@app.route('/influencer_register')
def add_influencer():
    return render_template('influencerregister.html')


@app.route('/isuccess', methods=['POST'])
def isuccess():
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    result = request.form
    list = []
    for key, value in result.items():
        list.append(value)
    dump = ('''INSERT INTO INFLUENCER VALUES(?,?,?,?,?,?,?,?,"")''')
    cursor.execute(dump, list)
    conn.commit()
    return render_template('log.html',RES="User Registered Successfully")


@app.route('/influencer_login')
def influencer_login():
    return render_template('influencerlogin.html')


@app.route('/influencer_dashboard', methods=['POST'])
def influencer_dashboard():
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    result = request.form
    credentials = []
    for key, value in result.items():
        credentials.append(value)
    cursor.execute('''SELECT USERNAME FROM INFLUENCER''')
    username = cursor.fetchall()
    arr_username = []
    for i in username:
        arr_username += i
    if credentials[0] in arr_username:
        cursor.execute('''SELECT PASSWORD FROM INFLUENCER WHERE USERNAME=?''', (str(credentials[0]),))
        password = cursor.fetchone()
        if credentials[1] in str(password):
            user = "http://127.0.0.1:5000/influencer_profile" + "/%s" % credentials[0]
            return redirect(user)
        else:
            return render_template("log.html",RES="Wrong Password")
    else:
        return render_template("log.html",RES="Invalid User")


@app.route('/influencer_profile/<string:user>', methods=['GET'])
def influencer_profile(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM INFLUENCER WHERE USERNAME=?''', (user,))
    det = cursor.fetchall()
    details = []
    for i in det:
        details += i
    return render_template('influencerdashboard.html', USER=user, FIRST_NAME=details[0],
                           LAST_NAME=details[1], EMAIL_ID=details[2], USERNAME=details[3], PASSWORD=details[4],
                           CATEGORY=details[5], POSITION=details[6], REACH=details[7], FLAG=details[8])


@app.route('/update_influencer/<string:user>')
def update_influencer(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM INFLUENCER WHERE USERNAME=?''', (user,))
    det = cursor.fetchall()
    details = []
    for i in det:
        details += i
    return render_template('influencerupdate.html', USER=user, FNAME=details[0], LNAME=details[1], EMAIL=details[2],
                           USERNAME=details[3], PASSWORD=details[4], CATEGORY=details[5], POSITION=details[6],
                           REACH=details[7],FLAG=details[8])


@app.route('/save_update_influencer/<string:user>', methods=['POST'])
def save_update_influencer(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    res = request.form
    list = []
    for key, value in res.items():
        list.append(value)
    list.append(user)
    dump = (
        '''UPDATE INFLUENCER SET FIRST_NAME=?, LAST_NAME=?, USERNAME=?, EMAIL_ID=?, PASSWORD=?, CATEGORY=?, POSITION=?, REACH=? WHERE USERNAME=?''')
    cursor.execute(dump, list)
    conn.commit()
    user = list[2]
    red = 'http://127.0.0.1:5000/influencer_profile/' + '%s' % user
    return redirect(red)


@app.route('/active_campaign/<string:user>', methods=['POST', 'GET'])
def active_campaign(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    details = cursor.execute('''SELECT C.SPONSOR_USERNAME, C.CAMPAIGN_NAME,C.DESCRIPTION,C.END_DATE,C.BUDGET,C.FLAG,
    CR.REQUEST FROM CAMPAIGN AS C,CAMPAIGN_REQUEST AS CR WHERE C.VISIBILITY="PUBLIC" AND 
    C.CAMPAIGN_NAME=CR.CAMPAIGN_NAME''').fetchall()
    res = cursor.execute('''SELECT FLAG FROM INFLUENCER WHERE USERNAME=?''',(user,)).fetchone()
    return render_template('activecampaign.html', USER=user, DETAILS=details, RES=res[0])


@app.route('/influencer_request_campaign/<string:user>', methods=['POST'])
def influencer_request_campaign(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    result = request.form
    l = []
    l1 = []
    for key, value in result.items():
        l.append(key)
        l1.append(value)
    l.append("Pending")
    l.append(user)
    cursor.execute(
        '''UPDATE CAMPAIGN_REQUEST SET SPONSOR_USERNAME=?, REQUEST=?, REQUEST_PERSON='I',INFLUENCER_USERNAME=? WHERE CAMPAIGN_NAME=?''',
        (l[0], l[1], l[2], l1[0]))
    conn.commit()
    val = "http://127.0.0.1:5000/active_campaign/" + "%s" % user
    return redirect(val)


@app.route('/influencer_requests/<string:user>', methods=['POST','GET'])
def influencer_requests(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    details = cursor.execute(
        '''SELECT CR.CAMPAIGN_NAME, C.DESCRIPTION, C.END_DATE, C.BUDGET,C.FLAG, CR.SPONSOR_USERNAME, CR.REQUEST, CR.REQUEST_PERSON FROM CAMPAIGN_REQUEST AS CR, 
        CAMPAIGN AS C WHERE CR.INFLUENCER_USERNAME=? AND CR.CAMPAIGN_NAME=C.CAMPAIGN_NAME''',(user,)).fetchall()
    return render_template('influencerrequest.html', USER=user, DETAILS=details)


@app.route('/influencer_save_requests/<string:user>', methods=['POST'])
def influencer_save_requests(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    res = request.form
    l = []
    for key, value in res.items():
        l.append(value)
        l.append(key)
    l.append(user)
    cursor.execute('''UPDATE CAMPAIGN_REQUEST SET REQUEST=? WHERE CAMPAIGN_NAME=? AND INFLUENCER_USERNAME=?''', (l))
    if l[0]=="DECLINE":
        cursor.execute('''UPDATE CAMPAIGN SET VISIBILITY="PUBLIC" WHERE CAMPAIGN_NAME=? AND INFLUENCER_USERNAME=?''', (l[1],l[2],))
        cursor.execute('''UPDATE CAMPAIGN SET INFLUENCER_USERNAME="" WHERE CAMPAIGN_NAME=? AND INFLUENCER_USERNAME=?''', (l[1],l[2],))
    conn.commit()
    val = "http://127.0.0.1:5000/influencer_requests/" + "%s" % user
    return redirect(val)


@app.route('/sponsor_register')
def add_sponsor():
    return render_template('sponsorregistration.html')


@app.route('/ssuccess', methods=['POST'])
def ssuccess():
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    result = request.form
    list = []
    for key, value in result.items():
        list.append(value)
    dump = ('''INSERT INTO SPONSOR VALUES(?,?,?,?,?,"")''')
    cursor.execute(dump, list)
    conn.commit()
    return render_template('log.html',RES="User Registered Successfully")


@app.route('/sponsor_login')
def sponsor_login():
    return render_template('sponsorlogin.html')


@app.route('/sponsor_dashboard', methods=['POST'])
def sponsor_dashboard():
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    result = request.form
    credentials = []
    for key, value in result.items():
        credentials.append(value)
    cursor.execute('''SELECT COMPANY_USERNAME FROM SPONSOR''')
    username = cursor.fetchall()
    arr_username = []
    for i in username:
        arr_username += i
    if credentials[0] in arr_username:
        cursor.execute('''SELECT PASSWORD FROM SPONSOR WHERE COMPANY_USERNAME=?''', (str(credentials[0]),))
        password = cursor.fetchone()
        if credentials[1] in str(password):
            user = "http://127.0.0.1:5000/sponsor_profile" + "/%s" % credentials[0]
            return redirect(user)
        else:
            return render_template("log.html",RES="Wrong Password")
    else:
        return render_template("log.html",RES="Invalid User")


@app.route('/sponsor_profile/<string:user>', methods=['GET'])
def sponsor_profile(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM SPONSOR WHERE COMPANY_USERNAME=?''', (user,))
    det = cursor.fetchall()
    details = []
    for i in det:
        details += i
    return render_template('sponsordashboard.html', USER=user, COMPANY_NAME=details[0], COMPANY_USERNAME=details[1],
                           EMAIL_ID=details[2], PASSWORD=details[3], INDUSTRY=details[4], FLAG=details[5])


@app.route('/update_sponsor/<string:user>')
def update_sponsor(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM SPONSOR WHERE COMPANY_USERNAME=?''', (user,))
    det = cursor.fetchall()
    details = []
    for i in det:
        details += i
    return render_template('sponsorupdate.html', USER=user, Cname=details[0], Uname=details[1], Semail=details[2],
                           Spassword=details[3], Ind=details[4], flag=details[5])


@app.route('/save_update_sponsor/<string:user>', methods=['POST', 'GET'])
def save_update_sponsor(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    res = request.form
    list = []
    for key, value in res.items():
        list.append(value)
    list.append(user)
    dump = (
        '''UPDATE SPONSOR SET COMPANY_NAME=? , COMPANY_USERNAME=? , EMAIL_ID=? , PASSWORD=? , INDUSTRY=? WHERE COMPANY_USERNAME=?''')
    cursor.execute(dump, list)
    cursor.execute('''UPDATE CAMPAIGN_REQUEST SET SPONSOR_USERNAME=? WHERE SPONSOR_USERNAME=?''',(list[1],user))
    conn.commit()
    user = list[1]
    red = 'http://127.0.0.1:5000/sponsor_profile/' + '%s' % user
    return redirect(red)


@app.route('/sponsor_mycampaign/<string:user>')
def sponsor_mycampaign(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT CAMPAIGN_NAME,DESCRIPTION,END_DATE,BUDGET,VISIBILITY,INFLUENCER_USERNAME,FLAG FROM CAMPAIGN WHERE SPONSOR_USERNAME=?''',
        (user,))
    result = cursor.fetchall()
    cursor.execute('''SELECT FIRST_NAME, LAST_NAME, EMAIL_ID, USERNAME, CATEGORY, POSITION, REACH, FLAG FROM INFLUENCER''')
    res = cursor.fetchall()
    return render_template('sponsormycampaign.html', RESULT=result, RES=res, USER=user)


@app.route('/sponsor_createcampaign/<string:user>')
def sponsor_createcampaign(user):
    return render_template('sponsorcreatecampaign.html', USER=user)


@app.route('/sponsor_save_createcampaign/<string:user>', methods=['POST'])
def sponsor_save_createcampaign(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    res = request.form
    result = []
    for key, value in res.items():
        result.append(value)
    if len(result) == 5:
        result.append("")
    cursor.execute('''INSERT INTO CAMPAIGN VALUES(?,?,?,?,?,?,?,"")''',
                   (user, result[0], result[1], result[2], result[3], result[4], result[5]))
    cursor.execute('''INSERT INTO CAMPAIGN_REQUEST(CAMPAIGN_NAME,SPONSOR_USERNAME,REQUEST) VALUES(?,?," ")''',
                   (result[0], user))
    conn.commit()
    val = "http://127.0.0.1:5000/sponsor_mycampaign/" + "%s" % user
    return redirect(val)


@app.route('/sponsor_save_mycampaign/<string:user>', methods=['POST'])
def sponsor_save_mycampaign(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    result = request.form
    values = []
    keys = []
    for key, value in result.items():
        values.append(value)
        keys.append(key)
    if keys[0] == "influencer":
        cursor.execute('''UPDATE CAMPAIGN SET VISIBILITY='PRIVATE', INFLUENCER_USERNAME=? WHERE CAMPAIGN_NAME=?''',
                       (values[0], values[1]))
        cursor.execute(
            '''UPDATE CAMPAIGN_REQUEST SET REQUEST='Pending',REQUEST_PERSON="S", INFLUENCER_USERNAME=? WHERE CAMPAIGN_NAME=?''',
            (values[0], values[1]))
    elif keys[0] == "rinfluencer":
        cursor.execute('''UPDATE CAMPAIGN SET VISIBILITY='PUBLIC', INFLUENCER_USERNAME="" WHERE CAMPAIGN_NAME=?''',
                       (values[-1],))
        cursor.execute(
            '''UPDATE CAMPAIGN_REQUEST SET REQUEST=" ",REQUEST_PERSON="", INFLUENCER_USERNAME="" WHERE CAMPAIGN_NAME=?''',
            (values[-1],))
    if keys[-1] == "del":
        cursor.execute('''DELETE FROM CAMPAIGN WHERE CAMPAIGN_NAME=?''', (values[-1],))
        cursor.execute('''DELETE FROM CAMPAIGN_REQUEST WHERE CAMPAIGN_NAME=?''', (values[-1],))
    conn.commit()
    val = "http://127.0.0.1:5000/sponsor_mycampaign/" + "%s" % user
    return redirect(val)


@app.route('/sponsor_requests/<string:user>')
def sponsor_requests(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    details = cursor.execute(
            '''SELECT CR.CAMPAIGN_NAME, C.DESCRIPTION, C.END_DATE, C.BUDGET,C.FLAG, CR.INFLUENCER_USERNAME, CR.REQUEST, 
            CR.REQUEST_PERSON FROM CAMPAIGN_REQUEST AS CR, CAMPAIGN AS C WHERE CR.SPONSOR_USERNAME=? AND 
            CR.CAMPAIGN_NAME=C.CAMPAIGN_NAME''',(user,)).fetchall()
    return render_template('sponsorrequest.html', USER=user, DETAILS=details)


@app.route('/sponsor_save_requests/<string:user>', methods=['POST'])
def sponsor_save_requests(user):
    conn = sqlite3.connect('sponsor_influencer.db')
    cursor = conn.cursor()
    res = request.form
    l = []
    for key, value in res.items():
        l.append(value)
        l.append(key)
    l.append(user)
    cursor.execute('''UPDATE CAMPAIGN_REQUEST SET REQUEST=? WHERE CAMPAIGN_NAME=? AND SPONSOR_USERNAME=?''', l)
    cursor.execute('''SELECT INFLUENCER_USERNAME FROM CAMPAIGN_REQUEST WHERE CAMPAIGN_NAME=?''', (l[1],))
    i = cursor.fetchone()
    if l[0]=="ACCEPT":
        cursor.execute('''UPDATE CAMPAIGN SET VISIBILITY="PRIVATE" WHERE CAMPAIGN_NAME=? AND SPONSOR_USERNAME=?''', (l[1], l[2],))
        cursor.execute('''UPDATE CAMPAIGN SET INFLUENCER_USERNAME=? WHERE CAMPAIGN_NAME=? AND SPONSOR_USERNAME=?''', (i[0],l[1],l[2],))
    val = "http://127.0.0.1:5000/sponsor_requests/" + "%s" % user
    conn.commit()
    return redirect(val)


@app.route('/logout')
def logout():
    conn = sqlite3.connect('sponsor_influencer.db')
    conn.close()
    return index()


app.run(debug=True)
