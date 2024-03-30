from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template( 'index.html' )

@app.route('/diary', methods=['GET'])
def show_diary():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'message': 'data received all good!!!'})

@app.route('/diary', methods=['POST'])
def add_to_diary():
    sample_receive = request.form.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': 'data was saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)