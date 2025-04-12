# 応援熱量可視化プロジェクト
オンラインライブにおける上肢運動の認識・画面表現の検証

### Project Structure
![image](https://github.com/user-attachments/assets/d4ead70e-7507-45ff-bbac-541feb80e875)
![image](https://github.com/user-attachments/assets/7c4b1d26-16ef-4975-8297-f4886ac70c30)


### How to deploy
1. Clone this repository, treat this repo as root
2. `pip install -r requirements.txt` on both computers
3. Sender side : ensure ip address of the receiver is correctly configured`python -m src.sender.main`
4. Receiver side : `python -m src.receiver.main --video {music title}`

### Phase Locking Value Algorithm
consitency of the phase difference beween two signals over time
1. Input: r(t), s(t) # receiver/sender hand Y-corodinates 0.05(sampling freq) * past 100 datapoints = 過去5秒間におけるY座標の変化
2. Apply Hilbert Transformation # scipy.signal.Hilbert()
3. Compute Instantenous Phase # np.angle()
4. Computer Phase Difference # np.arctan2(np.sin(delta), np.cos(delta))
5. Compute PLV # np.abs(np.sum(np.exp(1j * phase_diff))) / len(phase_diff)

- Blue -> low PLV
- Red -> high PLV
