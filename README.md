# Sistema de Detecção com Zona de Alerta

Detecta pessoas via webcam e avisa quando alguém entra em uma zona demarcada na tela — a mesma lógica por trás de boa parte das câmeras de segurança industrial, só que rodando em Python com YOLOv8.

## Demo
[gif/vídeo aqui]

## Por que esse projeto
Rodar `model.predict(show=True)` já detecta objeto, mas não decide nada sobre o que foi detectado. Eu queria ir um passo além: pegar a detecção e aplicar uma regra em cima — "essa pessoa está onde não devia?" — que é basicamente o primeiro degrau de qualquer sistema de monitoramento real.

## Como funciona
Em vez de deixar o Ultralytics desenhar tudo sozinho, o código lê frame a frame manualmente, roda a detecção, pega o centro da bounding box de cada pessoa detectada, e checa se esse ponto caiu dentro do retângulo da zona de risco. Se caiu, zona e caixa ficam vermelhas e aparece um aviso na tela.

Pra evitar que o alerta fique piscando toda vez que a detecção falha por um frame (o que acontece bastante em tempo real), só confirma o alerta depois de 5 frames seguidos com detecção dentro da zona — e só desarma depois de 5 frames seguidos sem. Simples, mas resolve a instabilidade sem precisar de nada mais elaborado.

Também apanhei um pouco no começo: sem `cv2.waitKey()` chamado a cada frame, a janela simplesmente trava. Não tem nada a ver com capturar tecla — é o que avisa o sistema operacional que a janela ainda está "viva".

E a zona hoje é calculada como proporção do frame, não em pixel fixo — na primeira versão eu tinha travado as coordenadas numa resolução específica e, óbvio, quebrava assim que testava em outra câmera.

## O que eu vi testando
Pessoa e cachorro: detecta bem, sem drama. Já celular, carteira e estojo viviam se confundindo entre si dependendo do ângulo — faz sentido, são objetos pequenos e retangulares parecidos, e o modelo aprende padrão visual, não "o que é" o objeto de fato. Por isso a lógica de alerta ficou restrita só à classe `person`; as outras classes continuam aparecendo na tela, só não disparam nada.

Rodei com `yolov8m.pt` e confiança mínima 0.4, e ficou fluido em tempo real, sem precisar trocar pro modelo nano.

## Stack
Python, OpenCV, Ultralytics YOLOv8

## Rodando localmente
\`\`\`bash
pip install ultralytics opencv-python
python webcam_deteccao.py
\`\`\`
Os pesos do modelo não estão no repo — o Ultralytics baixa sozinho na primeira vez que roda.

## Ideias pra continuar
- Trocar a webcam por uma câmera fixa em cenário real
- Fine-tuning em classes específicas (EPI, veículos, etc.)