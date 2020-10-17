import subprocess
import tempfile
import json

import falcon

from ingredient_phrase_tagger.training import utils

model_path = './models/ingredients.crfmodel'


def tag(ingredient_phrase):
    with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8') as input_file:
        input_file.write(utils.export_data(ingredient_phrase))
        input_file.flush()
        processOutput = subprocess.check_output(
            ['crf_test', '--verbose=1', '--model', model_path,
             input_file.name]).decode('utf-8')
        return utils.import_data(processOutput.split('\n'))


class ParseResource:
    def on_post(self, req, resp):
        ingredientPhrases = req.media['ingredientPhrases']
        tagged = [
            {
                'input': x['input'],
                'qty': x.get('qty', None),
                'unit': x.get('unit', None),
                'name': x.get('name', None),
                'other': x.get('other', None),
                'comment': x.get('comment', None),
            }
            for x in tag(ingredientPhrases)
        ]
        resp.body = json.dumps(tagged, indent='\t', sort_keys=True)


application = falcon.API()

application.add_route('/parse', ParseResource())
