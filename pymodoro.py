import os
import sys
import threading
import time
import tkinter as tk

SECONDS_IN_A_MINUTE = 60
MAIN_TIME_FRACTION = 0.8
REMAINING_TIME_FRACTION = 0.2


def dnd_on():
    from termcolor import colored
    print colored ("DND on", attrs=['bold']) #used bold to draw audience's eyes in 4/22
    time.sleep(5)  # Delaying so that our notification about DND ON started appears on screen ;)
    os.system("do-not-disturb on")


def dnd_off():
    print("Do not disturb off") #used to tell readers DND is off 4/22
    os.system("do-not-disturb off")


def show_end():
    root = tk.Tk()
    root.title("Pymodoro")
    window_width = 800
    window_height = 500
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    # position the window in the center of the page 
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, position_right, position_down))
    label = tk.Label(root, text="Pomodoro finished.\nTake a break!")
    label.place(x=window_width/2, y=window_height/2, anchor="center")
    label.config(font=("Courier", 60))
    tk.mainloop()


def speak(msg):
    os.system("pomodoro has finished, please take a break") #speaking message to the user 4/22


def notify(titlehas, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


minutes = int(sys.argv[1])
options = sys.argv[2:]

sound_on = "--no-sound" not in options
popup_on = "--no-popup" not in options


try:
    notify_thrd = threading.Thread(target=notify, args=("Pymodoro", f"Pomodoro started! You have {minutes} minutes."))
    notify_thrd.start()

    if sound_on:
        x = threading.Thread(target=speak,
                             args=(f"say pomodoro started, you have {minutes} minutes, DND on",))
        x.start()

    print(f"Pomodoro started, you have {minutes} minutes")
    dnd_on_thrd = threading.Thread(target=dnd_on)
    dnd_on_thrd.start()

    main_minutes = round(MAIN_TIME_FRACTION * minutes)
    remaining_minutes = round(REMAINING_TIME_FRACTION * minutes)

    for minute in range(main_minutes):
        print(f"{minutes - minute} minutes left")
        time.sleep(SECONDS_IN_A_MINUTE)

    # System notification
    # FIXME Experimenting
    os.system print colored ("do-not-disturb off",'yellow''bold') #added colors to the ending text to draw audiene eyes 4/22
    notify("Pymodoro", f"Pomodoro: {remaining_minutes} minutes left.")
    time.sleep(5)
    os.system("do-not-disturb on")

    if sound_on:
        x = threading.Thread(target=speak,
                             args=(f"say {remaining_minutes} minutes left in the pomodoro",))
                             args=(f"say you can do it!!") #added a motivational statement for the user 4/22
        x.start()

    for minute in range(remaining_minutes):
        print(f"{remaining_minutes - minute} minutes left") 
        time.sleep(SECONDS_IN_A_MINUTE)

    print("Pomodoro finished")
    dnd_off()
    if sound_on:
        x = threading.Thread(target=speak,
                             args=("say DING DING DING, pomodoro finished, DND off - take a break",))
        x.start()
    if popup_on:
        show_end()
except (KeyboardInterrupt, SystemExit):
    print("\n")
    dnd_off()
    print colored("You've successfully interrupted a pomodoro. Goodbye!",'Yellow'[bold]) #used to draw users eyes 4/22
