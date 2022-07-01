from aiogram import Bot, Dispatcher, types, executor

from db import *
from script import *

from random import randint

"""
due to how slow dalle mini is I didn't bother making anything async
"""

bot = Bot(token="")
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def starter(msg: types.Message):
    check_user = find_user_chat_id(int(msg.chat.id))
    if check_user:
        await msg.answer("dalle mini on telegram, the best meme generator. Send in your image desc as such\n /image cat swimming\n please be responsible with what you type other people will see what you request for.\n the code is available at https://github.com/msalbrain/dalle_in_telegram.git", disable_web_page_preview=True)
    else:
        A = User(chat_id=msg.chat.id,name=msg.chat.full_name)
        insert_user(A)
        await msg.answer("dalle mini on telegram, the best meme generator. Send in your image desc as such\n /image cat swimming\n please be responsible with what you type other people will see what you request for.\n the code is available at https://github.com/msalbrain/dalle_in_telegram.git", disable_web_page_preview=True)

def rnd_num(num, user_num):
    num1 = randint(1, num)
    while num1 == user_num:
        num1 = randint(1, num)

    return num1


@dp.message_handler(commands="image")
async def make_im_req(msg: types.Message):
    """
    due to how slow dalle mini is I didn't bother making anything async
    """
    us = find_user_chat_id(int(msg.chat.id))
    las_t = int(us.last_time)
    print(us.chat_id)
    if unix_time() - las_t < 180:
        pass
    else:
        print("i reached here")
        img_text = msg.text
        if len(img_text.split(" ")) < 2:
            await msg.answer("add your image description after the /image command \n  /image cat swimming")
        elif len(img_text.split(" ")) >= 2:
            get_desc = " ".join(img_text.split(" ")[1:])
            print("i also got here")
            g = first_image(get_desc)
            if g:
                await msg.answer_photo(g)
                f = find_all()
                if f:
                    num = rnd_num(f, us.id)
                    p = find_user_id(id=num)
                    await bot.send_photo(chat_id=p.chat_id, photo=g, caption=f"user {msg.chat.full_name} requested for {get_desc}")
                else:
                    pass
            else:
                await msg.answer("couldn't anything of your description")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)


