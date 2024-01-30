from flask import Flask, render_template, request
from textranksumarry import summarizer
from summary import freqsummarizer

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze',methods=['GET','POST'])
def analyze():
    if request.method== 'POST':
        rawtext=request.form['rawtext']
        summary, original_txt, len_orig_txt, len_summary =summarizer(rawtext)
        freq_summary, freq_orig_txt, freq_len_orig, freq_len_summary = freqsummarizer(rawtext)
    return render_template('summary.html',summary=summary, original_txt=original_txt,len_orig_txt=len_orig_txt,len_summary=len_summary,
                           freq_summary=freq_summary,freq_orig_txt=freq_orig_txt, freq_len_orig=freq_len_orig, freq_len_summary=freq_len_summary)


if __name__ =="__main__":
    app.run(debug=False,host='0.0.0.0')
