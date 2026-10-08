# Ising Project Presentation Example — speaker notes

[Google Slides](https://docs.google.com/presentation/d/1KAFb_y9PtoIpSW4TPFgb8FJGoKyu-NY-hI6zPfiZNhQ/edit)

15 main slides / 600 seconds; 7 backup slides.

## 1. Monte Carlo Simulation of the 2D Ising Model

발표 시간: 10초 | 구성: question

도입 10초. 실제 자성체의 자기 모멘트가 어떻게 집단적으로 정렬되고 가열에 어떻게 반응하는지 묻는다. 수업 계산을 활용한 중간발표 예시이며 새 학생 연구 성과라고 소개하지 않는다. 본문 15장 10분, 이후 7장은 질문에 답하기 위한 보충 자료다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 2. Motivation: magnetic order

발표 시간: 30초 | 구성: question

실제 물리적 동기 30초. 왼쪽은 NdFeB 영구자석 재료의 Kerr 현미경 사진이다. 결정립 안의 밝고 어두운 영역은 서로 다른 자화 방향의 자구이며, 이미 정렬된 영역이 있어도 서로 반대 방향이면 전체 자화가 상쇄될 수 있다. 사진 전체의 밝기를 자화의 크기로 해석하지 않는다. 오른쪽은 층상 자성체 CrI3 박편의 광학 사진이다. 이 사진은 시료의 형상을 보여주며 자화를 직접 찍은 것이 아니다. Huang 등의 논문은 단층에서 면밖 방향의 Ising형 강자성을 보고했다. 이 두 계는 국소 모멘트의 집단적 정렬과 낮은 차원이라는 물리적 질문을 제기한다. 아직 이번 프로젝트의 시뮬레이션 결과는 보여주지 않는다. NdFeB 자구의 형태나 CrI3의 전이온도를 본 정사각 격자 모형으로 예측하지 않는다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/
Gorchy, NdFeB-Domains.jpg, CC BY-SA 3.0: https://commons.wikimedia.org/wiki/File:NdFeB-Domains.jpg
License: https://creativecommons.org/licenses/by-sa/3.0/ ; no image alteration; original 20 micrometre scale bar retained.
B. Huang et al., Nature 546, 270–273 (2017), doi:10.1038/nature22391, Fig. 1c: https://www.nature.com/articles/nature22391/figures/1
Huang image: panel c cropped only; original 3 micrometre scale bar retained; optical image, not magnetic contrast.

## 3. Thermal disordering in two dimensions

발표 시간: 20초 | 구성: question

질문 20초. 교환 상호작용은 이웃의 정렬을 선호하고, 열적 요동은 더 많은 배열을 탐색하게 한다. 낮은 차원에서 이 경쟁이 어떤 집단적 행동을 만드는지 이해하기 위해 가장 단순한 모형을 쓴다. 계산 가능한 구체적인 질문은 정사각 유한 격자에서 평균 절댓값 자화가 온도에 따라 어떻게 변하는가이다. 유한 격자에서 급격하지만 매끈한 변화가 가능함을 설명하되 결과의 모양이나 수치를 여기서 미리 보여주지 않는다. 무한계 전이의 정확한 결정은 이번 질문의 범위가 아니다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 4. Square-lattice Ising model

발표 시간: 30초 | 구성: method

모형 30초. 강한 일축 이방성으로 허용 방향을 위와 아래 두 상태로 단순화한다. 작은 그림은 주기 경계의 연결을 보여주는 4×4 예시이며 시뮬레이션 결과가 아니다. 각 스핀은 네 최근접 이웃과만 상호작용하고, 파란 결합은 한 스핀의 네 이웃을 강조한다. 점선은 반대쪽 경계가 연결됨을 뜻한다. 양의 균일 교환결합, 영자기장, 고정된 스핀 크기를 쓴다. CrI3는 honeycomb 격자이며 본 수업 모형은 정사각 격자다. 장거리 dipolar 상호작용과 물질별 교환상수는 포함하지 않으므로 실제 자구 형태나 전이온도를 정량 예측하지 않는다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 5. Hamiltonian and Boltzmann sampling

발표 시간: 30초 | 구성: method

에너지 30초. 해밀토니안의 합은 서로 이웃한 결합을 한 번씩만 센다. 같은 방향의 한 결합은 -J, 반대 방향은 +J다. 따라서 스핀을 뒤집으면 이웃과의 정렬 여부에 따라 에너지가 변한다. 평형에서 배열의 확률은 Boltzmann 가중치로 정해지며 Z는 모든 배열에 대한 정규화 합이다. 온도가 높아지면 에너지가 높은 배열에 대한 억제가 약해진다. 에너지 최소화만 하면 열적 평형을 얻을 수 없으므로 Monte Carlo 표본추출이 필요하다. 계산에서는 J=kB=1을 쓰며 plot의 온도는 무차원 kBT/J다. 외부장 항은 영이라 제외했다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 6. Magnetization as the order parameter

발표 시간: 30초 | 구성: method

관측량 30초. M은 전체 스핀의 합, m은 스핀당 자화다. 작은 그림은 수동으로 구성한 세 배열이며 온도별 계산 결과가 아니다. 모두 위와 모두 아래는 자화 부호가 반대지만 둘 다 완전히 정렬되어 있다. 같은 수의 위와 아래가 있으면 전체 자화는 영이다. 영자기장 유한계에서 충분히 양쪽 방향을 표본추출하면 signed 평균은 상쇄되므로 먼저 매 측정의 절댓값을 구한 뒤 평균한다. 평균을 먼저 취하고 절댓값을 씌우는 것과 다르다. 식의 K는 한 run에 저장한 측정 개수다. 실측 run마다 평균을 하나 만들고 네 독립 run 사이의 표준오차를 보고한다. 절댓값 자화는 유한계의 정렬 지표이며 유한계 양의 값 자체를 무한계 자발자화의 증거로 해석하지 않는다. 표본 평균은 평형 기대값의 추정이므로 수식에 근사 기호를 쓴다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 7. Metropolis Monte Carlo

발표 시간: 30초 | 구성: method

전체 알고리즘 30초. 각 크기와 각 온도에 대해 독립 seed로 네 run을 수행한다. 짝수 run은 정렬 초기상태, 홀수는 무작위 초기상태다. 각 sweep은 전체 스핀 수만큼 위치를 무작위로 선택하여 단일 반전을 제안한다. 네 결합으로 에너지 차이를 구하고 Metropolis 규칙으로 수락하거나 현재 상태를 유지한다. 처음 8000 sweep은 버리고, 이후 5 sweep마다 현재 배열의 에너지와 signed 자화를 저장하여 16000개의 측정을 얻는다. 거절된 제안도 시도 횟수에 포함되며 기록 시점을 수락 사건에만 맞추면 안 된다. run별 절댓값 자화 평균을 만든 뒤 네 run의 평균과 run 간 표준오차를 보고한다. 큰 격자는 모든 배열을 열거할 수 없으므로 국소 Markov chain을 사용한다. 아래 코드는 흐름을 나타내는 의사코드다. 실제 한 sweep 코드는 Backup: Metropolis sweep에 있다. 일정한 discard 길이가 충분한지는 별도 수렴 검증 대상이다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 8. Result: Temperature dependence of magnetization

발표 시간: 90초 | 구성: results

핵심 결과 90초. 가이드의 순서대로 축, 비교 조건, 변화, 물리적 의미를 설명한다. 가로축은 reduced temperature, 세로축은 평균 절댓값 자화. L=16, 영자기장과 주기 경계에서 12개 온도를 비교한다. 네 독립 run의 평균과 표준오차다. 낮은 온도 1.5에서 약 0.987, 높은 온도 3.5에서 약 0.124로 감소한다. 낮은 온도의 정렬이 가열하면서 약해진다는 질문의 답이다. 점 사이 선은 fit이 아니다. 이 한 크기의 둥근 변화에서 정확한 임계온도를 읽지 않는다. 8,000 sweep discard, 다섯 sweep마다 16,000회 측정. 자세한 입력은 Backup: production settings에 있다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 9. Monte Carlo versus exact enumeration

발표 시간: 80초 | 구성: results

스핀이 아홉 개면 가능한 배열은 512개뿐이다. 각각의 에너지와 자화를 구한 뒤 Boltzmann 확률을 곱해서 평균하면 Monte Carlo 없이 정확한 평형값을 얻는다. 표의 Exact sum이 그 값이다. 같은 3×3 주기 격자를 Monte Carlo로 계산한 평균과 비교하면 세 온도에서 모두 표본 오차 범위 안에서 일치한다. 이 비교로 구현이 맞는지 확인한다. Monte Carlo 조건은 온도별 8개 독립 run, 1000 sweep 제외, 3 sweep마다 16000회 측정, seed 200–207이며 초기 상태는 모두 아래다. 큰 격자에서는 2의 스핀수 승만큼 배열 수가 늘어나 같은 직접합을 할 수 없어 표본추출을 쓴다. 이 작은 격자의 일치만으로 큰 격자의 평형화까지 확인되는 것은 아니다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 10. Statistical uncertainty

발표 시간: 70초 | 구성: results

표본 오차 70초. T=2.30, L=16의 독립 run 네 개를 한 점씩 보여준다. 선은 run 평균들의 평균, 음영은 그 평균의 표준오차다. 따라서 앞 결과 그림의 오차막대가 어떤 반복 계산에서 나왔는지 설명할 수 있다. 연속 측정은 서로 상관되어 있으므로 64,000개 측정을 모두 독립 반복처럼 세지 않는다. 이 추정은 run 사이 표본 변동을 나타낸다. 평형화 편향과 유한 크기 효과를 포함하지 않으며 run이 네 개뿐이라 오차 추정 자체도 제한적이다. 길이를 늘렸을 때의 안정성은 아직 검증하지 않았다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 11. Finite-size dependence

발표 시간: 60초 | 구성: interpretation

물리 해석 60초. 낮은 온도에서는 결합 에너지를 낮추는 정렬 상태가 우세하고 가열하면 뒤집힌 스핀을 포함한 여러 배열을 표본추출하면서 절댓값 자화가 작아진다. 세 크기의 비교에서 큰 격자의 변화가 더 가파르고 높은 온도의 잔여 자화가 작다. 작은 배열에서는 위아래 스핀 수의 차이만으로 양의 절댓값 자화가 남을 수 있다. 따라서 유한계의 양의 절댓값 자화를 곧바로 무한계의 자발자화로 해석하지 않는다. 이는 같은 저장 scan에서 실제로 확인한 크기 비교이며 기말에 수행할 수렴검증 전체를 대신하지 않는다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 12. Numerical limitations

발표 시간: 60초 | 구성: interpretation

세 격자 크기의 곡선은 같지 않다. 유한 크기에서 전이는 둥글게 나타나므로 한 곡선의 기울기만으로 임계온도를 정할 수 없다. 전이 부근에서는 국소 갱신의 완화가 느려 초기 배열의 영향이 오래 남을 수 있다. 연속 표본도 서로 상관되므로 측정점 수만 늘린다고 정보가 그만큼 늘지는 않는다. 정렬/무작위 초기상태를 비교하고 버리는 구간과 총 길이를 늘려 평균이 안정적인지 확인해야 한다. 그 다음 더 큰 격자와 촘촘한 온도점으로 급격한 변화를 살핀다. 현재 production scan에 대해 이 길이 검사는 아직 하지 않았다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 13. Outlook: thermal and magnetic response

발표 시간: 20초 | 구성: conclusion

다음 단계는 온도와 자기장을 조금 바꿀 때 계가 얼마나 반응하는지 계산하는 것이다. c는 외부장을 고정했을 때 스핀당 비열이며 전체 에너지의 변동으로 구한다. 기존 Ising II와 실행 자료에는 비열 환산이 있으므로 후속 작업은 크기별 봉우리의 위치와 높이를 비교하고 온도점을 보강하는 일이다. 자화율은 온도를 고정한 채 모형장 h를 가했을 때 signed 자화가 변하는 기울기다. h는 에너지 단위이며 실제 Tesla 단위 장과 같지 않다. 장이 있으면 전체 에너지는 E(0)-hM이다. 여기서 T는 물리 온도이며 기존 그림의 가로축은 kBT/J이다. 코드에서는 J=kB=1을 사용한다. 자화율 변동식에는 부호 있는 자화를 쓰며 절댓값 자화를 대입하지 않는다. 영자기장 유한계는 두 자화 방향 사이의 전환도 포함하므로 저온 표본추출을 충분히 해야 한다. 새로 작은 양·음의 장에서 계산하고 장 세기를 줄이며 수치미분이 선형응답 범위에서 변동식과 맞는지 확인할 계획이다. 자화율 곡선이 임계점에서 반드시 봉우리를 갖는다고 미리 단정하지 않는다. 이 장은 후속 분석 계획이며 새 응답함수 결과를 제시한 것이 아니다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/
D. Tong, Statistical Physics, energy fluctuations and heat capacity: https://www.damtp.cam.ac.uk/user/tong/statphys/statmechhtml/S1.html
Course notebook notebooks/03_ising_model_2.ipynb: heat capacity per spin from the total-energy variance.
Definitions independently checked using exact 3x3 sums and finite differences; revision5/assets/physics-checks.json and qa/independent-design-review.json.

## 14. Outlook: spin domains and correlations

발표 시간: 20초 | 구성: conclusion

자화가 같아도 스핀 배열은 다를 수 있다. 두 그림은 모두 위와 아래 스핀 수가 같도록 만든 16×16 설명용 배열이며 Monte Carlo의 특정 온도 결과가 아니다. 왼쪽에는 반대 방향으로 정렬된 큰 영역 두 개가 있고, 오른쪽은 같은 수의 스핀을 무작위로 섞었다. 따라서 전체 자화 영이라는 한 숫자만으로 공간 구조를 알 수 없다. 다음 계산에서는 전이 부근에서 배열을 연속 저장해 자구가 생기고 사라지는 모습을 MC sweep에 따라 시각화한다. MC sweep은 알고리즘의 진행 순서이며 실제 물질의 시간에 대응한다고 주장하지 않는다. G(r)는 거리 r만큼 떨어진 스핀 쌍의 곱을 평형 표본과 기준 격자점에 대해 평균한 상관함수다. 이것으로 스핀 정렬이 어느 거리까지 이어지는지 정량화한다. 장거리 극한의 자화 성분과 유한 크기 효과를 함께 고려하며 상관길이 분석은 아직 수행하지 않았다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/
Hand-constructed states and checks: revision5/assets/illustrative_states.npz; make_assets.py; physics-checks.json.

## 15. Summary

발표 시간: 20초 | 구성: conclusion

연구 대상과 계산 방법, 얻은 결과, 후속 연구를 한 문장씩 정리하며 발표를 마친다. 2차원 Ising 모형을 Metropolis Monte Carlo로 계산했다. 가열하면 자화가 감소하고 큰 격자에서 변화가 더 가파르다. 유한 크기 계산이므로 열역학적 극한의 임계 특성을 확정했다고 말하지 않는다. 후속 연구는 비열과 자화율, 스핀 배열의 시각화, 공간 상관함수다. 새 응답함수와 공간 상관 결과는 아직 제시하지 않았다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 16. Backup: Metropolis sweep

보충 자료: 10분 본문 밖

질문: 한 sweep은 어떻게 구현되는가? 모든 배열의 수가 스핀 수에 대해 지수적으로 늘어나므로 16×16에서는 전수조사 대신 Boltzmann 분포를 표본추출한다. 무작위 단일 스핀 제안과 Metropolis 수락 규칙을 설명한다. 에너지가 내려가면 항상 수락하고 올라가면 온도 의존 확률로 수락한다. 거절 시 현재 배열을 유지한다. 아래 코드는 기존 sweep의 핵심과 난수 호출 순서를 그대로 옮겼다. 한 sweep은 N번의 시도다. 국소 변화는 바뀐 네 결합으로 계산하므로 매번 전체 에너지를 다시 계산할 필요가 없다. 코드 줄을 읽지 말고 이 선택이 평형 분포를 표본추출하기 위한 것임을 설명한다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 17. Backup: energy updates

보충 자료: 10분 본문 밖

질문: 국소 에너지 갱신이 맞는지 어떻게 확인했는가? 답: 3×3의 모든 512개 배열에서 모든 스핀을 뒤집어 4,608번 전체 에너지 차이와 비교했다. 가능한 다섯 에너지 변화만 있으므로 그림에는 다섯 점이 나타나고 숫자는 중복 횟수다. 41,472개 controlled 수락/거절 조건도 확인했다. 평형화 검증과는 구분한다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 18. Backup: one spin flip

보충 자료: 10분 본문 밖

질문: 온도는 어떤 제안을 더 자주 수락하게 만드는가? 네 이웃이 모두 위인 중심 스핀을 뒤집으면 네 결합이 불리해져 8J 증가한다. 수락 확률은 T=1.5에서 약0.0048, T=3.5에서 약0.102이다. 이 값은 특정 제안의 수락확률이며 전체 run의 평균 수락률이 아니다. 거절하면 같은 배열을 유지하고 다음 시도로 진행한다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 19. Backup: production settings

보충 자료: 10분 본문 밖

질문: 다시 실행하려면 어떤 입력이 필요한가? 원자료 크기축은 8,16,32이고 본문 중심은16이다. 12개 온도는 1.5,2.0,2.1,2.15,2.2,2.25,2.3,2.35,2.4,2.5,3.0,3.5. seed는 20260917+10000L+100b+r, b는 온도 인덱스, r은0부터3까지의 run 인덱스다. 짝수 r은 정렬, 홀수 r은 무작위 초기 배열이다. seed 및 난수 순서를 보존한 L=8,T=2.30,r=1의 energy와 magnetization 16,000개가 원자료와 정확히 일치한다. 이는 재현성 검사이며 수렴성 증거가 아니다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 20. Backup: Binder cumulant

보충 자료: 10분 본문 밖

질문: 자화 분포로부터 무엇을 비교할 수 있는가? Binder cumulant는 부호에 영향을 받지 않는 둘째와 넷째 모멘트를 사용한다. 네 run마다 비율을 계산한 뒤 그 추정치를 평균한 것이 현재 그림의 정의다. 표본을 모두 pooling해서 비율을 만드는 것과 유한 표본에서 다를 수 있다. 이는 기말 보강의 한 예이며 본문 질문에 답하는 필수 추가 과제는 아니다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 21. Backup: Binder crossings

보충 자료: 10분 본문 밖

저장 scan의 이웃 크기쌍 crossing은 둘 다2.25–2.30 구간 안에서 선형 보간하면 약2.26이다. 원 계산의 보간값은2.259990과2.259920이다. 그 자릿수에 해당하는 정확도를 주장하지 않는다. 2.25–2.30은 샘플링한 온도격자 구간이며 신뢰구간이 아니다. 정밀 추정에는 더 세밀한 온도점·표본 오차 전파·크기 효과 확인이 필요하다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/

## 22. Backup: reproducibility and sources

보충 자료: 10분 본문 밖

가이드의 재현성·AI 공개 항목에 대응한다. 코드와 입력 자료는 기존 수업 Ising I/II에서 왔다. 이번 구성, 새 동반 노트북과 그림 재현 코드, 문구 정리와 자동 검증에 OpenAI Codex를 사용했다. 학생이 독립적으로 수행한 새 연구라고 표현하지 않는다. README에는 질문, 환경, 실행법, 입력·seed·sampling, 그림 재현, 검증·한계, 출처·AI 도움을 기록한다. 새 커널 전체 실행, 저장값 재현, 파일 해시와 native화면 검토를 완료했다. 제출 위치와 접근 권한은 학생에게 공지한 저장소 지침을 따른다. 이 예시의 공개 저장소 업로드는 별도로 수행하지 않았으므로 공개됐다고 설명하지 않는다. 도입의 실제 물질 사진은 계산 그림과 구분한다. NdFeB 자구 사진은 Gorchy의 CC BY-SA 3.0 원본, CrI3 광학 사진은 Huang 등 Nature 546, 270–273 (2017)의 Fig. 1c 발췌이며 해당 슬라이드 노트와 revision4/assets/provenance.json에 출처 및 변경 범위를 기록했다.

Sources
https://docs.google.com/presentation/d/1QsOKRrhFUsqKM46-rxKICXcGC6mP0_5u62APazEqQOk/edit
Course notebooks: notebooks/02_ising_model_1.ipynb; notebooks/03_ising_model_2.ipynb
Production data: notebooks/03_ising_model_2_data.npz
Exact benchmark: qa/notebooks/03_ising_model_2/physics.json
Companion package: outputs/2026-10-08/ising-project/ising-project-example/
