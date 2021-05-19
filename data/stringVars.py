#embed strings
dmFooter = 'Use Mentions that are given above the embed to navigate to those channels if you are useing a mobile device, you will see @Invalid-User inplace of user mention,use the web/desktop version to interact with it'
dmErrNotInDB ="The value you entered doesnt correspond to a message in the DB"
dmErrTimeout = "You took too long to provide the requested information."
dmErrInvalidInput = "The value enterd by you is not an integer."
dmErrFail = 'Failed to send DM!'
#----------------------------------------------------------------------------------------------------------------

#on message text

onMsg = '''Thank you for showing intrest in verification.
The Moderators will check your submission and if everything is in order they will verify else they will contact you
If DM is off Moderators will mention you in {}
Keep an eye on the {} chanel 
{}'''
onMsgNoAttachment = "There was no attachment in your message {} the content of your message was forwarded to the moderators"
#----------------------------------------------------------------------------------------------------------------


#string vars in listeners.py
errCmdNotFound = 'Please use a valid command\nUse <prefix>--h/botinfo/help to see list of commands.'
errMissingPerms = "Sorry {}, you do not have permissions to do that!Stop messing with me 😡 😡 🤬 🤬"
errUserNotFound = 'In place of mentioning a user you have used something else'
errFixValue ='Use <prefix>--h/botinfo/help to know more about commands'
errMemberNotFound = 'In place of mentioning a member in your Server/Guild you have used something else'
errMissingArguments ="A required argument was missing"
errRoleNotFound = 'In place of mentioning a role you have used something else'
errCriticalError = 'Please Send this mesage along with the command you used to the bot owner'
errTooManyArguments = "You have passed more that required argumnets"
oops = "Opps You did a mistake!!!!"


#string vars in moderation.py



#strings in messaging.py
dmErrNomsg = "Please provide the required message after mentioning me to add them to Message List"



#strings in modification.py
delSetupDelete = "Verification channel setup with\n{} as Listening Channel\n{} as Forwarding Channel\n{} as verified nottification Channel\n{} as General Nottification Channel\nhas been removed"
delSetupLFDelete = "simple listening forwarding channel setup with\n{} as Listening Channel\n{} as Forwarding Channel\nhas been removed"
setupLCexist = 'Listening channel {} alredy exist in DB,Hence another Forwarding channel cannot be setup. If you wish to reconfigure this Listening channel delet existing one using delete command then add again'
setupDone = "Verification channel setup with\n{} as Listening Channel\n{} as Forwarding Channel\n{} as verified nottification Channel\n{} as General Nottification Channel "
setupLFDone = "Listening Forwarding channel setup with\n{} as Listening Channel\n{} as Forwarding Channel\nis setup"









#----------------------------------------------------------------------------------------------------------------
#description 
#messaging.py
Des_help_dm = '''Used to send a dm to the specified user through the bot
Uasge : <prefix>dm <mention user > [message]
message is optional if no message is provided list of message from the database is given to you as a choice
If you want to add message to message list write the message after mentioning the Bot
If you wish to see the message list type msglist after mentioning the Bot
If you wish to delete a message from  message list type delete after mentioning the bot
'''
Des_help_send = '''Used to send message to a channel through the bot
Uasge : <prefix>send <mention channel > [message]
message is optional if no message is provided list of message from the database is given to you as a choice
To manipulate the messages in DB use the dm command
'''
#moderation.py
Des_help_gr = '''To give role to a member
Uasge : <prefix>['giveRole','gr','giverole','GiveRole'] <mention user > <mention role >
'''
Des_help_rr = '''To remove role from a member
Uasge : <prefix>['removeRole','rr','removerole','RemoveRole'] <mention user > <mention role >
'''
Des_help_roles = "To get the roles of a user\nUsage : <prefix>roles <mention user>"

Des_help_verify = '''Used to verify a user
Uasge : <prefix>['verify','v']  <mention User > <mention Rolel > <mention verified Channel > <Message(optional)>
Role :Role which the verified member will get
User : The person whom you want to give role
verified Channel : Channel where members are mentioned about their verification status
Message : optional message that you wish to include if none msg list will be shown type -1 to ignore it and send without message
A succesfull verification message will be send to mentioned channel and same will be send as dm to the user
'''
#modification.py
Des_help_delete = '''Used to delete Listening setup\nUasge : <prefix>sdelete <Mention channel>
This can be used to delete both verification setup and simple listening forwarding setup'''
Des_help_setPrefix = "Used to change the prefix of the bot\nUasge : <prefix>sp <new prefix>\n if no prefix is given default value of '.vb ' is  used"
Des_help_setup = '''Used to setup verification setup
Uasge : <prefix>setup <mention Listening Channel > <mention Forwarding Channel > <mention verified Channel > <mention General Channel >
Listening Channel :channel where members send images/tetx
Forwarding Channel : where you want the member message to be forwarded
verified Channel : Channel where members are mentioned about their verification status
General Channel : general chat channel of the server where members can be mentioned
'''
Des_help_setupLF = '''Used to setup simple listening forward channel
Uasge : <prefix>setup <mention Listening Channel > <mention Forwarding Channel > 
Listening Channel :channel where members send images/tetx
Forwarding Channel : where you want the member message to be forwarded
'''
#test.py
Des_help_ping = "To get ping value\n if multiple ping is recived please inform bot owner"
#----------------------------------------------------------------------------------------------------------------
# help 
#messaging.py
help_dm = "To send Dm to a member in your server"
help_send = "To send a message to a channel"
#moderation.py
help_gr = "To give role to a member"
help_rr ="To remove role from a member"
help_roles = "To see roles of a member"
help_verify = "To give member verified role/or role of your choice"
#modification.py
help_delete = "To delete Verification setup"
help_setPrefix = "To set prefix"
help_setup = "To setup verification setup"
help_setupLF = "To setup a simple listening forwarding channel"
#test.py
help_ping = "To get ping value"
#----------------------------------------------------------------------------------------------------------------

#help_botinfo = "To get advanced help"


#help_verify ="To verify a user"






