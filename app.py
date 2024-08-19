from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Dummy data for demonstration
CROP_SUGGESTIONS = {
    'clay': ['Wheat', 'Rice', 'Barley'],
    'sandy': ['Corn', 'Potatoes', 'Carrots'],
    'loamy': ['Tomatoes', 'Cucumbers', 'Lettuce']
}

SOIL_DATA = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def handle_form_submission():
    action = request.form.get('action')
    soil_type = request.form.get('soil_type')
    pH = request.form.get('pH')
    moisture = request.form.get('moisture')
    image = request.files.get('image')

    if action == 'recommend_crops':
        # Provide crop recommendations based on soil type
        recommended_crops = CROP_SUGGESTIONS.get(soil_type.lower(), [])
        if recommended_crops:
            response = {"message": f"Recommended crops for {soil_type} soil type: {', '.join(recommended_crops)}."}
        else:
            response = {"message": "No recommendations available for the specified soil type."}
    elif action == 'add_soil_data':
        # Add soil data to the list
        soil_data_entry = {"soil_type": soil_type, "pH": pH, "moisture": moisture}
        SOIL_DATA.append(soil_data_entry)
        response = {"message": f"Soil data added: {soil_data_entry}"}
    elif action == 'identify_disease':
        if image:
            # Save the image file
            image.save(f'uploads/{image.filename}')
            response = {"message": "Disease identification completed with uploaded image."}
        else:
            response = {"message": "No image uploaded."}
    else:
        response = {"message": "Invalid action specified."}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
