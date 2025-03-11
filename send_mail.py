def send_mail(smtp,port,sender,password,receiever,subject,data):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # html table with network device data
    html = """
    <html>
    <head>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
    </head>
    <body>
    <table>
        <tr>
            <th>Time</th>
            <th>MACAddress</th>
            <th>IPv4</th>
            <th>Interface</th>
            <th>Manufacturer</th>
        </tr>
    """
    for device in data:
        html += f"""
        <tr>
            <td>{device['Time']}</td>
            <td>{device['MACAddr']}</td>
            <td>{device['IPv4']}</td>
            <td>{device['Int']}</td>
            <td>{device['Manu']}</td>
        </tr>
        """
    html += """
    </table>
    </body>
    </html>
    """

    # building email message
    msg = MIMEMultipart()
    msg['From'] = f"{'netmon-lite'} <{sender}>"
    msg['To'] = ", ".join(receiever)
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))
    
    # sending the email to recipent using smtp relay
    with smtplib.SMTP(smtp, port) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
    print("Mail alert has been sent!")