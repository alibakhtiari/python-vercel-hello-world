from os.path import join
import qrcode
import ezdxf
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def generate_dxf():
    if request.method == "POST":
        data = request.form.get("data")
        model = request.form.get("model")
        serial = request.form.get("serial")

        # Read the existing DXF document
        file_path = "1.dxf"
        # file_path = join(dir, '..', 'data', '1.dxf')
        doc = ezdxf.readfile(file_path)

        # Generate QR code
        qr = qrcode.QRCode(
            version=10,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_matrix = qr.get_matrix()
        qr_size = len(qr_matrix)

        # Add a new layer for the QR code
        doc.layers.new(name="QRCode", dxfattribs={"color": 7})

        # Add the QR code to the DXF file
        msp = doc.modelspace()
        for y in range(qr_size):
            for x in range(qr_size):
                if qr_matrix[y][x]:
                    msp.add_polyline2d(
                        [(x+10, y), (x+10 + 1, y), (x+10 + 1, y + 1), (x+10, y + 1), (x+10, y)],
                        dxfattribs={"layer": "QRCode","insert": (720, 550)},
                    )

        # Add text to the DXF file
        text_style = "Arial"
        msp.add_text(
            model,
            dxfattribs={
                "layer": "Text",
                "style": text_style,
                "height": 30,
                "insert": (720, 550),
            },
        )

        # Save the modified DXF file
        output_file_path = "3.dxf"
        doc.saveas(output_file_path)

        return send_file(output_file_path, as_attachment=True)

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)