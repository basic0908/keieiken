# 応援熱量可視化プロジェクト
オンラインライブにおける上肢運動の認識・画面表現の検証

### Project Structure
![image](https://github.com/user-attachments/assets/d4ead70e-7507-45ff-bbac-541feb80e875)


### How to deploy
1. Clone this repository, treat this repo as root
2. `pip install -r requirements.txt` on both computers
3. Sender side : ensure ip address of the receiver is correctly configured`python -m src.sender.main`
4. Receiver side : `python -m src.receiver.main --video {music title}`

- Blue -> low PLV
- Red -> high PLV
