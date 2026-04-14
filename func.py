import streamlit as st
import pandas as pd
import random
from datetime import datetime
import io

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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{task_name}_{timestamp}.csv"
    
    # Фильтруем ответы по текущему заданию
    task_responses = {k: v for k, v in st.session_state.responses.items() if k.startswith(task_name)}
    
    if task_responses:
        data = []
        for question, answer in task_responses.items():
            data.append({"Вопрос": question, "Ответ": answer})
        
        df = pd.DataFrame(data)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        csv_string = csv_buffer.getvalue()
        
        
        # Показываем кнопку для скачивания
        st.download_button(
            label=f"📥 Скачать результаты задания {task_name}",
            data=csv_string.encode('utf-8-sig'),
            file_name=filename,
            mime="text/csv"
        )
        st.success(f"✅ Результаты задания {task_name} готовы к скачиванию!")
        return True
    else:
        st.info("Нет ответов для сохранения")
        return False

def save_all_results(st):
    """Сохраняет результаты всех заданий в один CSV файл"""
    from datetime import datetime
    import pandas as pd
    import io
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_all_tasks_{timestamp}.csv"
    
    if st.session_state.responses:
        data = []
        for question, answer in st.session_state.responses.items():
            data.append({"Вопрос": question, "Ответ": answer})
        
        df = pd.DataFrame(data)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        csv_string = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Скачать результаты ВСЕХ заданий",
            data=csv_string.encode('utf-8-sig'),
            file_name=filename,
            mime="text/csv"
        )
        st.success("✅ Результаты всех заданий готовы к скачиванию!")
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
    
    # СОЗДАЁМ СЛУЧАЙНЫЙ ПОРЯДОК
    indices = list(range(len(event_list)))
    
    # Используем key_prefix как seed для стабильного перемешивания
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
    
    return matching  # ЭТОТ RETURN ДОЛЖЕН БЫТЬ ВНУТРИ ФУНКЦИИ

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
