import json


from ..formproc.formproc import FormProducer
from ..routers.templates import Languages

class Invoker:
    root = "../../example/regsitration"

    @classmethod
    def test_form_filling( cls ):
        form = FormProducer(
            template=open( f"{ cls.root }/registration.xlsx" ),
            lang=Languages.English,
            localizations=json.load( f"{ cls.root }/translations.json" ),
            answer_data= json.load( f"{ cls.root }/answer.json" )
        )
        with ( open( "jp.pdf", "wb" ) as jp_dst,
               open( "local.pdf", "wb" ) as target_dst ):
            jp_dst.write( form.jp_doc )
            target_dst.write( form.target_doc )

Invoker.test_form_filling()