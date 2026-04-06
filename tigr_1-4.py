# для запуска нажать пуск справа, потом в создавшуюся консоль написать
# pipx run streamlit run /Users/avoka/PyCharmMiscProject/tigr_1-4.py
import streamlit as st
import task_data
import func

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
    index = len(st.session_state.responses)
    answ_co = len(task_data.person_easy)

    if index < answ_co:
        st.header("Задание 1")
        answer = func.render_task(st, task_data.person_easy[index], "easy", index, "Задание1")
        if answer is not None:
            st.session_state.responses[f"Задание 1: {task_data.person_easy[index]['stimulus_text']}"] = answer
            st.rerun()

        func.skip_task(st, index, answ_co, "Задание 1: ")
    else:
        st.header("Задание 1 завершено!")
        if st.button("Перейти к следующему заданию"):
            st.session_state.current_step = 4
            st.rerun()

# ==================== ЗАДАНИЕ 2 ====================
def render_task2(time_list, event_list, key_prefix):
    """Отображает задание на сопоставление"""
    
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
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Два столбца
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="task2-time"><h4>📅 Время</h4>', unsafe_allow_html=True)
        for i, t in enumerate(time_list):
            st.markdown(f'<div class="task2-item">{i+1}. {t}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="task2-event"><h4>📖 Событие</h4>', unsafe_allow_html=True)
        for i, e in enumerate(event_list):
            st.markdown(f'<div class="task2-item">{chr(65+i)}. {e}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Выпадающие списки
    matching = {}
    for i, time_text in enumerate(time_list):
        options = [f"{chr(65+j)}. {event_list[j]}" for j in range(len(event_list))]
        matching[i] = st.selectbox(
            f"Для «{time_text}» выберите событие:",
            options=options,
            key=f"{key_prefix}_match_{i}",
            index=None
        )
    
    return matching


if st.session_state.current_step == 4:
    st.header("Задание 2")
    st.markdown(
        """
        <style>.custom-text {font-size: 18px; line-height: 1.6; margin-bottom: 20px;}</style>
        <div class="custom-text">
            <p>Вы увидите 3 маркера времени и 3 предложения.</p>
            <p>Для каждого времени выберите соответствующее предложение из выпадающего списка.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Начать тренировку"):
        st.session_state.current_step = 5
        st.session_state.task2_test_index = 0
        st.rerun()

elif st.session_state.current_step == 5:
    index = st.session_state.task2_test_index
    
    if index < len(task_data.person_middle_minus_test):
        st.header("Тренировка задания 2")
        task = task_data.person_middle_minus_test[index]
        matching = render_task2(task["time"], task["event"], f"train2_{index}")
        
        if st.button("Далее"):
            if all(v is not None for v in matching.values()):
                st.session_state.task2_test_index += 1
                st.rerun()
            else:
                st.warning("Выберите все варианты")
    else:
        st.header("Тренировка задания 2 завершена!")
        if st.button("Перейти к заданию 2"):
            st.session_state.current_step = 6
            st.rerun()

elif st.session_state.current_step == 6:
    index = len([k for k in st.session_state.responses.keys() if k.startswith("Задание 2")])
    answ_co = len(task_data.person_middle_minus)
    
    if index < answ_co:
        st.header("Задание 2")
        task = task_data.person_middle_minus[index]
        matching = render_task2(task["time"], task["event"], f"task2_{index}")
        
        if st.button("Далее"):
            if all(v is not None for v in matching.values()):
                for i, time_text in enumerate(task["time"]):
                    st.session_state.responses[f"Задание 2: {time_text}"] = matching[i]
                st.rerun()
            else:
                st.warning("Выберите все варианты")
        
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
            <p>Вы увидите 6 строк, в которых нужно будет сформировать правильные предложения.</p>
            <p>Вам будет предложено начало предложения.</p>
            <p>Вам нужно будет из предложенных вариантов выбрать тот, который правильно завершает начало предложения.</p>
            <p>Сделать это нужно будет для всех предложений.</p>
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
        result = func.render_middle_minus_task(st, task, index, "train3")

        if st.button("Далее"):
            if all(v is not None for v in result.values()):
                st.session_state.task3_test_index += 1
                st.rerun()
            else:
                st.warning("Выберите все варианты перед переходом.")
    else:
        st.header("Тренировка задания 3 завершена!")
        if st.button("Перейти к заданию 3"):
            st.session_state.current_step = 9
            st.rerun()

elif st.session_state.current_step == 9:
    index = int(len([k for k in st.session_state.responses.keys() if k.startswith("Задание 3")]) / 6)
    answ_co = len(task_data.person_middle_plus)

    if index < answ_co:
        st.header("Задание 3")
        task = task_data.person_middle_plus[index]
        result = func.render_middle_minus_task(st, task, index, "Задание3")

        if st.button("Далее"):
            if all(v is not None for v in result.values()):
                for i, subject in enumerate(task["subjects"]):
                    st.session_state.responses[f"Задание 3 (итерация {index}): {subject}"] = result[i]
                st.rerun()
            else:
                st.warning("Выберите все варианты перед переходом.")

        func.skip_task(st, index * 6, answ_co * 6, "Задание 3: ")
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
            <p>В конце предложения будет написано одно слово в скобках.</p>
            <p>Это слово нужно вставить на место пропуска, изменив его форму так, чтобы предложение было грамматически верным.</p>
            <p>Вам нужно будет напечатать это слово в окошке для ввода ответа.</p>
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
