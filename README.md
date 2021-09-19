# Simple-Bubble-Bobble
pygame을 이용한 Bubble Bobble 게임입니다.

## Requirements
pygame 패키지를 설치해주세요.
```
pip install pygame
```

## How to Run
```main.py```를 실행해주세요.
```
python main.py
```

## How to Play the Game
버블을 발사하여 적을 버블 안에 가두세요. 버블에 가둔 후 터뜨리면 적을 물리칠 수 있습니다. 만약 제때 터뜨리지 못하여 버블이 천장까지 도달할 경우 버블 안에 갇힌 적은 부활하게 되며 한동안 무적상태가 됩니다.

### Player
![standing](https://user-images.githubusercontent.com/65074958/131250668-7bf9d105-07fe-4cb7-bc60-09ca04c6f79b.png)

조작키
* ← : 왼쪽으로 이동
* → : 오른쪽으로 아동
* ↑ : 점프
* space : 공격(버블 발사)

### Enemy
![reaper](https://user-images.githubusercontent.com/65074958/131250788-50405377-8537-4774-82cc-193cebe35259.png)
Level 1 Enemy (느림)
![reaper3](https://user-images.githubusercontent.com/65074958/131250803-f6da88f8-3ece-4dd6-a312-4bd4daa8c4bf.png)
Level 2 Enemy (보통)
![reaper4](https://user-images.githubusercontent.com/65074958/131250805-b56b73e1-aba6-4c3f-b2aa-37510c3592af.png)
Level 3 Enemy (빠름)
![reaper2](https://user-images.githubusercontent.com/65074958/131250797-c855347b-3bbb-4129-ab07-ddbc46c0f32d.png)
Level 4 Enemy (무적)

Level 4 Enemy는 버블에 갇히지 않는 무적 상태지만 대신 매우 느립니다. 무적 상태가 풀릴 때까지 피해 다니세요!
