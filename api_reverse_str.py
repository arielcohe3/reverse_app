from flask import Flask, jsonify, request

app = Flask(__name__)

result = None
last_result = None

@app.route('/reverse', methods=['GET'])
def reverse_string():
  """Reverses the order of words in a string.
    The input string is passed as a query parameter in the request.
    If the input string contains only
    one word, an error message is returned. Otherwise, the reversed string is returned as a JSON object.
    The reversed string is also stored in the global variable 'result' for future reference.
  """
  global result
  global last_result
  string = request.args.get('in')
  if len(string.split()) == 1:
    return jsonify({'error': 'Please provid more than 1 word'})
  result = " ".join(reversed(string.split()))
  # for scallability this state should be saved in a database
  last_result = result
  return jsonify({'result': result})

@app.route('/restore', methods=['GET'])
def restore_result():
    """Endpoint for restoring the last result.
    Returns:
        JSON object with the key 'result' and the value of the last result if it exists,
        or with the key 'error' and the value 'No previous result found' if it does not.
    """
    global last_result
    if last_result:
        return jsonify({'result': last_result})
    else:
        return jsonify({'error': 'No previous result found'})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
