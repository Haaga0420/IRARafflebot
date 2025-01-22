from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import requests
import random

# Bot token and group chat ID
TOKEN = '7745887063:AAHewy1tlGTFKlJOxQ_fEXYE0Z8Thg3ma9k'
GROUP_CHAT_ID = '@your_group_chat_id'

# Raffle settings
ENTRY_FEE = 10
PRIZE = 250
MAX_TICKETS = 30
CONTRACT_ADDRESS = '0x329633ed1ca833d0f1577aeffb8333bdb678b27f'
raffle_tickets = []
purchased_addresses = {}

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
def buyticket(update: Update, context: CallbackContext):
    remaining_tickets = MAX_TICKETS - len(raffle_tickets)
    message = (
        f"To purchase a raffle ticket:\n"
        f"Entry Fee: ${ENTRY_FEE}\n"
        f"Prize: ${PRIZE}\n"
        f"Remaining Tickets: {remaining_tickets}\n"
        f"Send payment to: {CONTRACT_ADDRESS}\n"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

buyticket_handler = CommandHandler('buyticket', buyticket)
dispatcher.add_handler(buyticket_handler)
def is_admin(user_id):
    # Implement your logic to check if the user is an admin
    return True

def setraffle(update: Update, context: CallbackContext):
    if is_admin(update.message.from_user.id):
        options = (
            "/setfee [amount] - Set ticket price\n"
            "/setprize [amount] - Set prize\n"
            "/setpayment [address] - Set contract address\n"
            "/setmax [number] - Set max tickets\n"
            "/lastwin - Display last winner\n"
            "/setgif - Upload image/gif\n"
        )
        context.bot.send_message(chat_id=update.message.from_user.id, text=options)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You do not have permission to use this command.")

setraffle_handler = CommandHandler('setraffle', setraffle)
dispatcher.add_handler(setraffle_handler)
const express = require('express');
const app = express();
app.use(express.json());

app.post('/webhook', (req, res) => {
    const transaction = req.body;
    // Process the transaction
    notifyGroup(transaction);
    res.status(200).send('Transaction received');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

function notifyGroup(transaction) {
    // Your logic to notify the group
    const remainingTickets = updateRaffleTickets(transaction);
    const message = `Ticket sold! ${remainingTickets} tickets remaining.`;
    sendMessageToGroup(message);

    if (remainingTickets === 0) {
        const winner = pickRandomWinner();
        const winnerMessage = `Congratulations ${winner}! You won the raffle prize of $250!`;
        sendMessageToGroup(winnerMessage);
        resetRaffle();
    }
}

function updateRaffleTickets(transaction) {
    // Logic to update raffle tickets
    raffle_tickets.push(transaction.from);
    purchased_addresses[transaction.from] = purchased_addresses.get(transaction.from, 0) + 1;
    return MAX_TICKETS - raffle_tickets.length;
}

function pickRandomWinner() {
    return raffle_tickets[random.randint(0, MAX_TICKETS - 1)];
}

function resetRaffle() {
    raffle_tickets = [];
    purchased_addresses = {};
}

function sendMessageToGroup(message) {
    const axios = require('axios');
    axios.post(`https://api.telegram.org/bot${TOKEN}/sendMessage`, {
        chat_id: GROUP_CHAT_ID,
        text: message
    });
}
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Raffle bot is now active.")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
