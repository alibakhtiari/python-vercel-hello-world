from os.path import join
import qrcode
import ezdxf
from sanic import Sanic
from sanic.response import file, html

app = Sanic(__name__)

@app.route("/", methods=["GET", "POST"])
async def generate_dxf(request):
    if request.method == "POST":
        data = request.form.get("data")
        model = request.form.get("model")
        serial = request.form.get("serial")

        # Read the existing DXF document
        # file_path = "1.dxf"
        file_path = join(dir, '..', 'data', '1.dxf')
        doc = ezdxf.readfile(file_path)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
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
                        [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x, y)],
                        dxfattribs={"layer": "QRCode"},
                    )

        # Add text to the DXF file
        text_style = "Arial"
        msp.add_text(
            model,
            dxfattribs={
                "layer": "Text",
                "style": text_style,
                "height": 40,
                "insert": (720, 550),
            },
        )

        # Save the modified DXF file
        output_file_path = "3.dxf"
        doc.saveas(output_file_path)

        return await file(output_file_path, filename="3.dxf")

    else:
        return html('''
            <html>
            <body>
            <form action="/" method="post" enctype="multipart/form-data">
                <label for="data">Data:</label><br>
                <input type="text" id="data" name="data"><br><br>
                <label for="model">Model:</label><br>
                <input type="text" id="model" name="model"><br><br>
                <label for="serial">Serial:</label><br>
                <input type="text" id="serial" name="serial"><br><br>
                <input type="submit" value="Generate DXF">
            </form>
            </body>
            </html>
        ''')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)