import streamlit as st
import pandas as pd


def skip_task(st, curr_index=int, max_index=int, task_name=str):
    st.markdown(
        """
        <style>
            .st-key-skip .stButton button {
                background-color: transparent;
                border: 2px solid red;
                padding: 10px 20px;
                border-radius: 5px;
                color: red;
                cursor: pointer;
                font-size: 14px;
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 1000;
                width: auto;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Пропустить задание", key="skip"):
        st.write(st.session_state.current_step)
        for i in range(curr_index + 1, max_index + 1):
            st.session_state.responses[f"{task_name}Cтимул{i}"] = 0
        st.rerun()


def save_and_download_result(st, task_name):
    """Сохраняет результаты и сразу предлагает скачать файл"""
    from datetime import datetime
    import pandas as pd
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{task_name}_{timestamp}.csv"
    
    # Фильтруем ответы по текущему заданию
    task_responses = {k: v for k, v in st.session_state.responses.items() if k.startswith(task_name)}
    
    if task_responses:
        df = pd.DataFrame(list(task_responses.items()), columns=["Вопрос", "Ответ"])
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        # Показываем кнопку для скачивания
        with open(filename, "rb") as f:
            st.download_button(
                label=f"📥 Скачать результаты задания {task_name}",
                data=f,
                file_name=filename,
                mime="text/csv"
            )
        st.success(f"✅ Результаты задания {task_name} готовы к скачиванию!")
        return True
    else:
        st.info("Нет ответов для сохранения")
        return False


# ==================== ФУНКЦИИ ДЛЯ РЕНДЕРИНГА ЗАДАНИЙ ====================

import random

def render_easy_task(st, task, task_index, task_name):
    """
    Отображение задания типа person_easy
    Формат: {'prime_text': str, 'stimulus_text': str, 'answers': tuple, 'hint': str}
    """
    # Получаем ответы
    answers = task['answers']
    merged_answers = []
    used_indices = set()

    for i, ans in enumerate(answers):
        if i in used_indices:
            continue

    # Обработка варианта с пометкой (а) - например "заболел(а)"
        if "(а)" in ans:
            base_word = ans.replace("(а)", "").strip()
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
            
            # мужской (заканчивается на "л") и женский (заканчивается на "ла")
            if ans.endswith("л") and answers[j].endswith("ла"):
                merged_answers.append(f"{ans}/{answers[j]}")
                used_indices.add(i)
                used_indices.add(j)
                merged = True
                break
            # женский (заканчивается на "ла") и мужской (заканчивается на "л")
            elif ans.endswith("ла") and answers[j].endswith("л"):
                merged_answers.append(f"{answers[j]}/{ans}")
                used_indices.add(i)
                used_indices.add(j)
                merged = True
                break
            # возвратные глаголы (лся/лась)
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
            
    # Перемешиваем ответы
    shuffled_answers = list(merged_answers)
    random.shuffle(shuffled_answers)
    
    st.write(f"**{task['prime_text']}**")
    st.write(task['stimulus_text'])
    
    if 'hint' in task and task['hint']:
        st.caption(f"💡 Подсказка: {task['hint']}")
    
    return st.radio(
        "Выберите правильный вариант:",
        options=shuffled_answers,
        key=f"{task_name}_{task_index}",
        index=None
    )


def render_middle_minus_task(st, task, task_index, task_name):
    """
    Отображение задания типа person_middle_minus (сопоставление времени и события)
    Формат: {'time': list, 'event': list}
    """
    st.write("**Соедините действия справа с правильными указаниями времени слева.**")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Время**")
        for i, time_text in enumerate(task['time']):
            st.write(f"{i + 1}. {time_text}")

    with col2:
        st.write("**Событие**")
        for i, event_text in enumerate(task['event']):
            st.write(f"{chr(65 + i)}. {event_text}")

    st.write("---")

    matching = {}
    for i, time_text in enumerate(task['time']):
        matching[i] = st.selectbox(
            f"Для '{time_text}' выберите событие:",
            options=list(range(len(task['event']))),
            format_func=lambda x, event_list=task['event']: f"{chr(65 + x)}. {event_list[x]}",
            key=f"{task_name}_{task_index}_match_{i}",
            index=None
        )

    return matching


def render_middle_plus_task(st, task, task_index, task_name):
    """
    Отображение задания типа person_middle_plus
    Формат: {'stimulus_text': str, 'answers': tuple}
    """
    st.write(task['stimulus_text'])

    return st.radio(
        "Выберите правильный вариант:",
        options=task['answers'],
        key=f"{task_name}_{task_index}",
        index=None
    )


def render_complex_task(st, task, task_index, task_name):
    """
    Отображение задания типа person_complex (ввод пропущенного слова)
    Формат: str (предложение с __ и глаголом в скобках)
    """
    st.write(task)

    return st.text_input(
        "Введите пропущенное слово в правильной форме:",
        key=f"{task_name}_{task_index}"
    )


def render_task(st, task, task_type, task_index, task_name):
    """
    Универсальная функция рендеринга задания в зависимости от типа
    task_type: 'easy', 'middle_minus', 'middle_plus', 'complex'
    """
    if task_type == "easy":
        return render_easy_task(st, task, task_index, task_name)
    elif task_type == "middle_minus":
        return render_middle_minus_task(st, task, task_index, task_name)
    elif task_type == "middle_plus":
        return render_middle_plus_task(st, task, task_index, task_name)
    elif task_type == "complex":
        return render_complex_task(st, task, task_index, task_name)
    else:
        st.error(f"Неизвестный тип задания: {task_type}")
        return None
