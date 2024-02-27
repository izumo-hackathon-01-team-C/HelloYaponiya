import json
import os
import asyncio


from ..formproc.formproc import FormProducer
from ..routers.templates import Languages

class Invoker:
    root = "example/registration"

    @classmethod
    async def test_form_filling( cls ):
        form = FormProducer(
            #os.listdir( os.getcwd() + "/example/registration" )
            template=open( f"{ cls.root }/registration.xlsx", "rb" ).read(),
            lang=Languages.English,
            localizations=json.load( open( f"{ cls.root }/translations.json", "r" ) ),
            answer_data= json.load( open( f"{ cls.root }/answer.json", "r" ) )
        )
        await form.execute()
        with ( open( "jp.pdf", "wb" ) as jp_dst,
               open( "local.pdf", "wb" ) as target_dst ):
            jp_dst.write( form.jp_doc )
            target_dst.write( form.target_doc )
        


async def main():
    await Invoker.test_form_filling()

asyncio.run(  main() )