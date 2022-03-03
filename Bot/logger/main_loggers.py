from imports import *
import utils


class Logger():

    def __init__(self):
        self.pytz = pytz.timezone('Europe/Berlin')
        self.time = datetime.datetime.now(tz=self.pytz)



    @utils.time_wrapper
    async def send_error_log(self, err, cmd):
        embed = discord.Embed(
            title=f"Ein Fehler ist aufgetreten! {type(err)}",
            description=err,
            color=discord.Colour.red(),
            timestamp=self.time,
        )
        embed.add_field(name="Command:", value=f"{cmd}")
        embed.add_field(name=f"Error:", value=f"{err}")

        trc_list = [i for i in traceback.TracebackException.from_exception(err).format()]
        filename = f'./extensions/err_logs/errorlog_{cmd}_{int(time.time())}.txt'
        with open(filename, 'w') as file:
            for i in trc_list:
                file.write(i)
        file = discord.File(filename)

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                'Webhook_URL',
                adapter=AsyncWebhookAdapter(session))

            await webhook.send(
                username='Error-Log',
                avatar_url="https://cdn-icons.flaticon.com/png/512/1008/premium/1008930.png?token=exp=1646310482~hmac=2727aa6e1ff8277825b326f620dc790f",
                embed=embed,
                file=file,
            )
