from rasa.nlu.components import Component
from spellchecker import SpellChecker


class SpellCheck(Component):

    def __init__(self, component_config=None):
        super(SpellCheck, self).__init__(component_config)

    @staticmethod
    def spell_check(txtStr):
        # txtStr=jobj.get("text")
        text = txtStr.split(' ')
        spell = SpellChecker()
        # print(text)

        corrected = ""

        for txt in text:
            misspelled = spell.unknown([txt])
            if txt in misspelled:
                corrected = corrected + spell.correction(txt)+" "
            else:
                corrected = corrected + txt + " "
        
        corrected = corrected.rstrip()
        
        resp = {
            "text": txtStr,
            "corrected": corrected
        }

        return resp

    def process(self, message, **kwargs):
        msg = message.text
        op = SpellCheck.spell_check(msg)
        print(op)
        message.text = op.get("corrected")
        