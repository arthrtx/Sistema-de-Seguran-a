import cv2 as cv
import os

from modulos.config import PASTA_FACES


def tirarFoto(username):
    pasta = str(PASTA_FACES)
    os.makedirs(pasta, exist_ok=True)

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a câmara.")
        return None

    print("====================================")
    print("Prima P para tirar a fotografia.")
    print("Prima Q para cancelar.")
    print("====================================")

    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        cv.imshow("Webcam", frame)

        key = cv.waitKey(1) & 0xFF

        if key == ord('p') or key == ord('P'):
            caminho = os.path.join(pasta, f"{username}.jpg")

            if cv.imwrite(caminho, frame):
                print("Foto guardada com sucesso!")
                cap.release()
                cv.destroyAllWindows()
                return caminho
            else:
                print("Erro ao guardar a fotografia.")
                cap.release()
                cv.destroyAllWindows()
                return None

        elif key == ord('q') or key == ord('Q'):
            print("Operação cancelada.")
            cap.release()
            cv.destroyAllWindows()
            return None

