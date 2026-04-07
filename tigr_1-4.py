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
    st.write(f"DEBUG: step=5, index={st.session_state.task2_test_index}")
    
    index = st.session_state.task2_test_index
    
    if index < len(task_data.person_middle_minus_test):
        st.header("Тренировка задания 2")
        
        task = task_data.person_middle_minus_test[index]
        
        # Показываем время и события
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Время:**")
            for i, t in enumerate(task["time"]):
                st.write(f"{i+1}. {t}")
        with col2:
            st.write("**Событие:**")
            for i, e in enumerate(task["event"]):
                st.write(f"{chr(65+i)}. {e}")
        
        st.markdown("---")
        
        # Выпадающие списки
        matching = {}
        for i, time_text in enumerate(task["time"]):
            options = [f"{chr(65+j)}. {task['event'][j]}" for j in range(len(task["event"]))]
            matching[i] = st.selectbox(
                f"Для «{time_text}» выберите событие:",
                options=options,
                key=f"train2_match_{i}_{index}",
                index=None
            )
        
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


# СТРАНИЦА 6: ОСНОВНОЕ ЗАДАНИЕ
elif st.session_state.current_step == 6:
    index = len([k for k in st.session_state.responses.keys() if k.startswith("Задание 2")])
    answ_co = len(task_data.person_middle_minus)
    
    if index < answ_co:
        st.header("Задание 2")
        
        task = task_data.person_middle_minus[index]
        
        # Показываем время и события
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Время:**")
            for i, t in enumerate(task["time"]):
                st.write(f"{i+1}. {t}")
        with col2:
            st.write("**Событие:**")
            for i, e in enumerate(task["event"]):
                st.write(f"{chr(65+i)}. {e}")
        
        st.markdown("---")
        
        # Выпадающие списки
        matching = {}
        for i, time_text in enumerate(task["time"]):
            options = [f"{chr(65+j)}. {task['event'][j]}" for j in range(len(task["event"]))]
            matching[i] = st.selectbox(
                f"Для «{time_text}» выберите событие:",
                options=options,
                key=f"task2_match_{i}_{index}",
                index=None
            )
        
        if st.button("Сохранить ответ"):
            if all(v is not None for v in matching.values()):
                for i, time_text in enumerate(task["time"]):
                    selected_letter = matching[i][0]
                    selected_index = ord(selected_letter) - 65
                    selected_event_text = task["event"][selected_index]
                    st.session_state.responses[f"Задание 2 (вопрос {index + 1}): {time_text}"] = selected_event_text
                st.rerun()
            else:
                st.warning("Выберите все варианты")
        
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
            <p>Вы увидите предложение с пропущенным глаголом.</p>
            <p>Вам необходимо выбрать правильную форму слова.</p>
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
            <p>После пропуска будет написано слово в скобках.</p>
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
