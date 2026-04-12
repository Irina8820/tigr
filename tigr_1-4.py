# для запуска нажать пуск справа, потом в создавшуюся консоль написать
# pipx run streamlit run /Users/avoka/PyCharmMiscProject/tigr_1-4.py
import streamlit as st
import task_data
import func
import random

# Инициализация состояния страницы
if "current_step" not in st.session_state:
    st.session_state.current_step = 0

if "responses" not in st.session_state:
    st.session_state.responses = {}

st.title("ТИГР: тренируемся изучать грамматику")

# ==================== СТРАНИЦА ПРИВЕТСТВИЯ ====================
if st.session_state.current_step == 0:
    st.header("Добро пожаловать в тест!")
    st.write("В этом тесте вам предстоит выполнить несколько заданий.")
    if st.button("Начать"):
        st.session_state.current_step = 1
        st.rerun()

# ==================== ЗАДАНИЕ 1 ====================
if st.session_state.current_step == 1:
    st.header("Задание 1")
    st.markdown(
        """
        <style>.custom-text {font-size: 18px; line-height: 1.6; margin-bottom: 20px;}</style>
        <div class="custom-text">
            <p>Вы увидите предложение с пропущенным глаголом.</p>
            <p>Над этим предложением вы увидите предложение-образец, опираясь на которое вам нужно будет заполнить пропуск.</p>
            <p>Из двух вариантов ответа вам нужно будет выбрать подходящий и нажать на него.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Начать тренировку"):
        st.session_state.current_step = 2
        st.session_state.training_index = 0
        st.rerun()

elif st.session_state.current_step == 2:
    # ТРЕНИРОВКА - БЕЗ ИЗМЕНЕНИЙ
    training_data = task_data.person_easy_test
    index = st.session_state.training_index

    if index < len(training_data):
        st.header("Тренировка задания 1")
        answer = func.render_task(st, training_data[index], "easy", index, "train1")
        if answer is not None:
            st.session_state.training_index += 1
            st.rerun()
    else:
        st.header("Тренировка задания 1 завершена!")
        if st.button("Перейти к заданию 1"):
            st.session_state.current_step = 3
            st.rerun()

elif st.session_state.current_step == 3:
    # ОСНОВНОЕ ЗАДАНИЕ - ИСПОЛЬЗУЕМ 50 СЛУЧАЙНЫХ ПРИМЕРОВ
    index = len(st.session_state.responses)
    answ_co = len(st.session_state.shuffled_task1)  # 50 случайных примеров

    if index < answ_co:
        st.header(f"Задание 1 (вопрос {index + 1} из {answ_co})")
        answer = func.render_task(st, st.session_state.shuffled_task1[index], "easy", index, "Задание1")
        if answer is not None:
            st.session_state.responses[f"Задание 1: {st.session_state.shuffled_task1[index]['stimulus_text']}"] = answer
            st.rerun()

        func.skip_task(st, index, answ_co, "Задание 1: ")
    else:
        st.header("Задание 1 завершено!")
        if st.button("Перейти к следующему заданию"):
            st.session_state.current_step = 4
            st.rerun()

# ==================== ЗАДАНИЕ 2 ====================
def render_task2(time_list, event_list, key_prefix):
    """Отображает задание на сопоставление со случайным порядком событий"""
    
    # Стилизация
    st.markdown(
        """
        <style>
            .task2-container {
                display: flex;
                gap: 40px;
                margin: 20px 0;
            }
            .task2-time, .task2-event {
                flex: 1;
                border: 2px solid orange;
                background-color: #ffebcc;
                padding: 15px;
                border-radius: 10px;
            }
            .task2-time h4, .task2-event h4 {
                text-align: center;
                margin: 0 0 15px 0;
            }
            .task2-item {
                padding: 10px;
                margin: 10px 0;
                background-color: white;
                border-radius: 5px;
                border-left: 4px solid orange;
            }
            .custom-text {
                font-size: 18px;
                line-height: 1.6;
                margin-bottom: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # СОЗДАЁМ СЛУЧАЙНЫЙ ПОРЯДОК (без random.shuffle)
    # Используем key_prefix как seed для стабильного перемешивания в рамках одного задания
    indices = list(range(len(event_list)))
    
    # Простое перемешивание на основе суммы символов key_prefix
    seed = sum(ord(c) for c in key_prefix) % 100
    for i in range(len(indices) - 1, 0, -1):
        j = (seed + i) % (i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    
    # Два столбца с дизайном
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="task2-time"><h4>📅 Время</h4>', unsafe_allow_html=True)
        for i, t in enumerate(time_list):
            st.markdown(f'<div class="task2-item">{i+1}. {t}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="task2-event"><h4>📖 Событие</h4>', unsafe_allow_html=True)
        for display_idx, original_idx in enumerate(indices):
            letter = chr(65 + display_idx)
            event_text = event_list[original_idx]
            st.markdown(f'<div class="task2-item">{letter}. {event_text}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Выпадающие списки
    matching = {}
    for i, time_text in enumerate(time_list):
        options = []
        for display_idx, original_idx in enumerate(indices):
            letter = chr(65 + display_idx)
            event_text = event_list[original_idx]
            options.append(f"{letter}. {event_text}")
        
        selected = st.selectbox(
            f"«{time_text}»:",
            options=options,
            key=f"{key_prefix}_match_{i}",
            index=None
        )
        
        if selected:
            selected_letter = selected[0]
            selected_display_idx = ord(selected_letter) - 65
            matching[i] = indices[selected_display_idx]
        else:
            matching[i] = None
    
    return matching


# СТРАНИЦА 4: ИНСТРУКЦИЯ
if st.session_state.current_step == 4:
    st.header("Задание 2")
    st.markdown(
        """
        <div class="custom-text">
            <p>Вы увидите три указателя времени (слева) и три события (справа).</p>
            <p>Вам необходимо соединить каждый указатель времени с соответствующим событием.</p>
            <p>Для каждого времени выберите подходящее событие из выпадающего списка.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Начать тренировку"):
        st.session_state.current_step = 5
        st.session_state.task2_test_index = 0
        st.rerun()


# СТРАНИЦА 5: ТРЕНИРОВКА
elif st.session_state.current_step == 5:
    index = st.session_state.task2_test_index
    
    if index < len(task_data.person_middle_minus_test):
        st.header("Тренировка задания 2")
        st.markdown(
            """
            <div class="custom-text">
                <p>Соедините время с событием</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        task = task_data.person_middle_minus_test[index]
        matching = render_task2(task["time"], task["event"], f"train2_{index}")
        
        if st.button("Далее"):
            if all(v is not None for v in matching.values()):
                st.session_state.task2_test_index += 1
                st.rerun()
            else:
                st.warning("Пожалуйста, выберите событие для каждого указателя времени.")
    else:
        st.header("Тренировка задания 2 завершена!")
        if st.button("Перейти к заданию 2"):
            st.session_state.current_step = 6
            st.rerun()


# СТРАНИЦА 6: ОСНОВНОЕ ЗАДАНИЕ
elif st.session_state.current_step == 6:
    index = len([k for k in st.session_state.responses.keys() if k.startswith("Задание 2")])
    answ_co = len(task_data.person_middle_minus)
    
    if index < answ_co:
        st.header("Задание 2")
        st.markdown(
            """
            <div class="custom-text">
                <p>Соедините указатели времени с соответствующими событиями.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        task = task_data.person_middle_minus[index]
        matching = render_task2(task["time"], task["event"], f"task2_{index}")
        
        if st.button("Далее"):
            if all(v is not None for v in matching.values()):
                for i, time_text in enumerate(task["time"]):
                    selected_event_text = task["event"][matching[i]]
                    st.session_state.responses[f"Задание 2 (вопрос {index + 1}): {time_text}"] = selected_event_text
                st.rerun()
            else:
                st.warning("Пожалуйста, выберите событие для каждого указателя времени.")
        
        # Кнопка пропуска
        func.skip_task(st, index, answ_co, "Задание 2: ")
    
    else:
        st.header("Задание 2 завершено!")
        if st.button("Перейти к следующему заданию"):
            st.session_state.current_step = 7
            st.rerun()
# ==================== ЗАДАНИЕ 3 ====================
if st.session_state.current_step == 7:
    st.header("Задание 3")
    st.markdown(
        """
        <style>.custom-text {font-size: 18px; line-height: 1.6; margin-bottom: 20px;}</style>
        <div class="custom-text">
            <p>Вы увидите предложение с пропущенным словом.</p>
            <p>Ниже будут представлены 3 варианта ответов</p>
            <p>Выберите правильную форму слова.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Начать тренировку"):
        st.session_state.current_step = 8
        st.session_state.task3_test_index = 0
        st.rerun()

elif st.session_state.current_step == 8:
    index = st.session_state.task3_test_index

    if index < len(task_data.person_middle_plus_test):
        st.header("Тренировка задания 3")
        
        task = task_data.person_middle_plus_test[index]
        stimulus = task["stimulus_text"]
        answers = task["answers"]
        
        # ОБЪЕДИНЯЕМ ВАРИАНТЫ С РАЗНЫМ РОДОМ
        merged_answers = []
        used_indices = set()
        
        for i, ans in enumerate(answers):
            if i in used_indices:
                continue
            
            # Обработка варианта с пометкой (а) - например "заболел(а)"
            if "(а)" in ans:
                # Превращаем "заболел(а)" в "заболел/заболела"
                base_word = ans.replace("(а)", "").strip()
                # Определяем мужской и женский вариант
                if base_word.endswith("л"):
                    masculine = base_word
                    feminine = base_word + "а"
                elif base_word.endswith("лся"):
                    masculine = base_word
                    feminine = base_word.replace("лся", "лась")
                else:
                    masculine = base_word
                    feminine = base_word + "а"
                merged_answers.append(f"{masculine}/{feminine}")
                used_indices.add(i)
                continue
            
            merged = False
            for j in range(i + 1, len(answers)):
                if j in used_indices:
                    continue
                
                # Вариант 1: мужской (заканчивается на "л") и женский (заканчивается на "ла")
                if ans.endswith("л") and answers[j].endswith("ла"):
                    merged_answers.append(f"{ans}/{answers[j]}")
                    used_indices.add(i)
                    used_indices.add(j)
                    merged = True
                    break
                # Вариант 2: женский (заканчивается на "ла") и мужской (заканчивается на "л")
                elif ans.endswith("ла") and answers[j].endswith("л"):
                    merged_answers.append(f"{answers[j]}/{ans}")
                    used_indices.add(i)
                    used_indices.add(j)
                    merged = True
                    break
                # Вариант 3: возвратные глаголы (лся/лась)
                elif ans.endswith("лся") and answers[j].endswith("лась"):
                    merged_answers.append(f"{ans}/{answers[j]}")
                    used_indices.add(i)
                    used_indices.add(j)
                    merged = True
                    break
                elif ans.endswith("лась") and answers[j].endswith("лся"):
                    merged_answers.append(f"{answers[j]}/{ans}")
                    used_indices.add(i)
                    used_indices.add(j)
                    merged = True
                    break
            
            if not merged:
                merged_answers.append(ans)
                used_indices.add(i)
        
        # Перемешиваем только один раз
        shuffle_key = f"shuffled_train3_{index}"
        if shuffle_key not in st.session_state:
            import random
            shuffled = list(merged_answers)
            random.shuffle(shuffled)
            st.session_state[shuffle_key] = shuffled
        
        shuffled_answers = st.session_state[shuffle_key]
        
        st.write(stimulus)
        
        choice = st.radio(
            "Выберите правильный вариант:",
            options=shuffled_answers,
            key=f"train3_{index}",
            index=None
        )
        
        if st.button("Далее"):
            if choice is not None:
                st.session_state.task3_test_index += 1
                del st.session_state[shuffle_key]
                st.rerun()
            else:
                st.warning("Пожалуйста, выберите ответ.")
    else:
        st.header("Тренировка задания 3 завершена!")
        if st.button("Перейти к заданию 3"):
            st.session_state.current_step = 9
            st.rerun()

elif st.session_state.current_step == 9:
    index = len([k for k in st.session_state.responses.keys() if k.startswith("Задание 3")])
    answ_co = len(task_data.person_middle_plus)

    if index < answ_co:
        st.header("Задание 3")
        
        task = task_data.person_middle_plus[index]
        stimulus = task["stimulus_text"]
        answers = task["answers"]
        
        # ОБЪЕДИНЯЕМ ВАРИАНТЫ С РАЗНЫМ РОДОМ
        merged_answers = []
        used_indices = set()
        
        for i, ans in enumerate(answers):
            if i in used_indices:
                continue
            
            # Обработка варианта с пометкой (а) - например "заболел(а)"
            if "(а)" in ans:
                # Превращаем "заболел(а)" в "заболел/заболела"
                base_word = ans.replace("(а)", "").strip()
                # Определяем мужской и женский вариант
                if base_word.endswith("л"):
                    masculine = base_word
                    feminine = base_word + "а"
                elif base_word.endswith("лся"):
                    masculine = base_word
                    feminine = base_word.replace("лся", "лась")
                else:
                    masculine = base_word
                    feminine = base_word + "а"
                merged_answers.append(f"{masculine}/{feminine}")
                used_indices.add(i)
                continue
            
            merged = False
            for j in range(i + 1, len(answers)):
                if j in used_indices:
                    continue
                
                # Вариант 1: мужской (заканчивается на "л") и женский (заканчивается на "ла")
                if ans.endswith("л") and answers[j].endswith("ла"):
                    merged_answers.append(f"{ans}/{answers[j]}")
                    used_indices.add(i)
                    used_indices.add(j)
                    merged = True
                    break
                # Вариант 2: женский (заканчивается на "ла") и мужской (заканчивается на "л")
                elif ans.endswith("ла") and answers[j].endswith("л"):
                    merged_answers.append(f"{answers[j]}/{ans}")
                    used_indices.add(i)
                    used_indices.add(j)
                    merged = True
                    break
                # Вариант 3: возвратные глаголы (лся/лась)
                elif ans.endswith("лся") and answers[j].endswith("лась"):
                    merged_answers.append(f"{ans}/{answers[j]}")
                    used_indices.add(i)
                    used_indices.add(j)
                    merged = True
                    break
                elif ans.endswith("лась") and answers[j].endswith("лся"):
                    merged_answers.append(f"{answers[j]}/{ans}")
                    used_indices.add(i)
                    used_indices.add(j)
                    merged = True
                    break
            
            if not merged:
                merged_answers.append(ans)
                used_indices.add(i)
        
        # Перемешиваем только один раз
        shuffle_key = f"shuffled_task3_{index}"
        if shuffle_key not in st.session_state:
            import random
            shuffled = list(merged_answers)
            random.shuffle(shuffled)
            st.session_state[shuffle_key] = shuffled
        
        shuffled_answers = st.session_state[shuffle_key]
        
        st.write(stimulus)
        
        choice = st.radio(
            "Выберите правильный вариант:",
            options=shuffled_answers,
            key=f"task3_{index}",
            index=None
        )
        
        if st.button("Сохранить ответ"):
            if choice is not None:
                st.session_state.responses[f"Задание 3 (вопрос {index + 1}): {stimulus}"] = choice
                del st.session_state[shuffle_key]
                st.rerun()
            else:
                st.warning("Пожалуйста, выберите ответ.")
        
        func.skip_task(st, index, answ_co, "Задание 3: ")
    
    else:
        st.header("Задание 3 завершено!")
        if st.button("Перейти к следующему заданию"):
            st.session_state.current_step = 10
            st.rerun()

# ==================== ЗАДАНИЕ 4 ====================
if st.session_state.current_step == 10:
    st.header("Задание 4")
    st.markdown(
        """
        <style>.custom-text {font-size: 18px; line-height: 1.6; margin-bottom: 20px;}</style>
        <div class="custom-text">
            <p>Вы увидите предложение с пропущенным словом.</p>
            <p>Рядом с пропуском будет написано слово (в скобках)</p>
            <p>Напечатайте пропущенное слово (в скобках) в подходящей форме.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Начать тренировку"):
        st.session_state.current_step = 11
        st.session_state.task4_test_index = 0
        st.rerun()

elif st.session_state.current_step == 11:
    index = st.session_state.task4_test_index

    if index < 3:
        st.header("Тренировка задания 4")
        answer = func.render_complex_task(st, task_data.person_complex_test[index], index, "train4")

        if st.button("Далее") and answer:
            st.session_state.task4_test_index += 1
            st.rerun()
    else:
        st.header("Тренировка задания 4 завершена!")
        if st.button("Перейти к заданию 4"):
            st.session_state.current_step = 12
            st.rerun()

elif st.session_state.current_step == 12:
    index = len([k for k in st.session_state.responses.keys() if k.startswith("Задание 4")])
    answ_co = len(task_data.person_complex)

    if index < answ_co:
        st.header("Задание 4")
        answer = func.render_complex_task(st, task_data.person_complex[index], index, "Задание4")

        if st.button("Далее") and answer:
            st.session_state.responses[f"Задание 4: {task_data.person_complex[index]}"] = answer
            st.rerun()

        func.skip_task(st, index, answ_co, "Задание 4: ")
    else:
        st.header("Задание 4 завершено!")
        func.save_result(st)
