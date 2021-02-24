def welcomePasswordEmail(user, password):
    return f'''
        <div>
            <h4>Dear {user.first_name} {user.last_name}</h4>
            <br/>
            <p>Welcome to the Lead CRM as an Agent</p>
            <p><b>Username:</b> {user.username}</p>
            <p><b>Password:</b> {password}</p>
            <p>Please change this temporary password as soon as possible</p>
            <br/>
            <p>Sincerly</p>
            <p>Support Team</p>
        </div>
    '''


def assignedLead(user):
    return f'''
        <div>
            <h4>Dear {user.first_name} {user.last_name}</h4>
            <br/>
            <p>A new lead has been assigned to you</p>
            <p>Login to Lead CRM to view the lead</p>
            <br/>
            <p>Sincerly</p>
            <p>Support Team</p>
        </div>
    '''
