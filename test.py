with open(".credentials") as file:
    for line in file:
        exec(line)

print(telegram_token)
print(dialogflow_token)
