from openai import OpenAI
import streamlit as st

st.title("Yotube text generator powered by gpt-4-0613, dall-e-3")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

TITLE_PROMPT = """
あなたはYoutubeの動画のタイトルの生成をします。
Youtubeで高評価数の多い動画のタイトルに似せて、
以下の記事を解説動画した1つのタイトルを生成してください。
記事タイトルは改行で分割されています。
引用元サイトの名前は出さないでください。
"""

DESCRIPTION_PROMPT = """
あなたはYoutubeの動画の概要の生成をします。
Youtubeで高評価数の多い動画の概要欄に似せて、
以下の複数の記事についての解説動画概要を生成してください。
記事タイトルは改行で分割されています。
記事タイトルに無い情報は使わないでください。
フレンドリーな文体にしてください。
"""

TAG_PROMPT = """
あなたはYoutubeの動画のタグの生成をします。
Youtubeで高評価数の多い動画のタグに似せて、
以下の複数の記事についての解説動画タグを生成してください。
記事タイトルは改行で分割されています。
記事タイトルに無い情報は使わないでください。
同じタグは生成しないでください。
タグは「,」で区切って列挙してください。
"""


THUMBNAIL_PROMPT_PLACEHOLDER = """e.g. 3匹のかわいい子猿が笑顔で温泉に入りながらMacBookでタイピングしている画像を生成してください。
空には火星が浮かんでいます。
文字は表示しないでください。"""

st.header("TEXT GENERATOR")
if prompt := st.text_area("enter article titles"):

    # Title
    stream = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": TITLE_PROMPT},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    st.subheader("Title")
    st.write_stream(stream)

    # Description
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": DESCRIPTION_PROMPT},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    st.subheader("Description")
    st.session_state.description = st.write_stream(stream)

    # Tags
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": TAG_PROMPT},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    st.subheader("Tags")
    st.session_state.tags = st.write_stream(stream)


st.header("THUMBNAIL GENERATOR")
if prompt := st.text_area(THUMBNAIL_PROMPT_PLACEHOLDER):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    st.image(image_url)