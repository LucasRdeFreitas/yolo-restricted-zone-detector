import cv2
from ultralytics import YOLO

modelo = YOLO('yolov8m.pt')

cap = cv2.VideoCapture(0)


ret, frame = cap.read()
if not ret:
    print("Não foi possível acessar a câmera.")
    cap.release()
    exit()

altura, largura = frame.shape[:2]
ZONA = (int(largura * 0.3), int(altura * 0.1), int(largura * 0.6), int(altura * 0.85))  # (x1, y1, x2, y2), proporcional ao frame

QUADROS_PARA_CONFIRMAR = 5   
contador_dentro = 0          
contador_fora = 0            
alerta_confirmado = False    

while True:
    ret, frame = cap.read()
    if not ret:
        break

    resultado = modelo.predict(frame, conf=0.4, verbose=False)[0]

    deteccao_bruta = False

    for caixa in resultado.boxes:
        classe = modelo.names[int(caixa.cls[0])]
        x1, y1, x2, y2 = map(int, caixa.xyxy[0])
        conf = float(caixa.conf[0])

        cor = (0, 200, 0)

        if classe == "person":
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            dentro_da_zona = (ZONA[0] <= cx <= ZONA[2]) and (ZONA[1] <= cy <= ZONA[3])

            if dentro_da_zona:
                cor = (0, 0, 255)
                deteccao_bruta = True

        cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
        texto = f"{classe} {conf:.0%}"
        cv2.putText(frame, texto, (x1, max(y1 - 8, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, cor, 2)

    if deteccao_bruta:
        contador_dentro += 1
        contador_fora = 0
    else:
        contador_fora += 1
        contador_dentro = 0

    if contador_dentro >= QUADROS_PARA_CONFIRMAR:
        alerta_confirmado = True
    if contador_fora >= QUADROS_PARA_CONFIRMAR:
        alerta_confirmado = False

    cor_zona = (0, 0, 255) if alerta_confirmado else (0, 165, 255)
    cv2.rectangle(frame, (ZONA[0], ZONA[1]), (ZONA[2], ZONA[3]), cor_zona, 2)

    if alerta_confirmado:
        cv2.putText(frame, "ALERTA: pessoa na zona", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("Teste", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()