from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    # We build the form directly in HTML. 
    # This is often MORE reliable than a Python redirect for PayFast.
    return render_template_string('''
        <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
            <h1>Finalize Mom's Website</h1>
            <p>Click the button below to test the R100 payment.</p>
            
            <form action="https://sandbox.payfast.co.za/eng/process" method="post">
                <input type="hidden" name="merchant_id" value="10000100">
                <input type="hidden" name="merchant_key" value="46f0cd694581a">
                <input type="hidden" name="amount" value="100.00">
                <input type="hidden" name="item_name" value="Consultation">
                
                <input type="submit" value="Pay with PayFast" 
                       style="padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 5px;">
            </form>
        </div>
    ''')

if __name__ == "__main__":
    app.run(debug=True, port=5005)



    