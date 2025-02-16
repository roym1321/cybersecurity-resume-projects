import discord
from discord import app_commands
import openai
from Tokens import KEY
from Init_Bot import bot
import random

openai.api_key = KEY


def image_variation_response(prompt, n=1):
    response = openai.Image.create_variation(
        image=prompt,
        n=n,
        response_format='url'
    )
    print(f"Created {len(response['data'])} image variations")
    return response['data']


def image_response(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        response_format='url'
    )
    return response['data'][0]['url']


def ai_response(prompt, model_engine="gpt-3.5-turbo") -> str:
    messages = [{"role": "system", "content": prompt}]
    try:
        completions = openai.ChatCompletion.create(
            model=model_engine,
            messages=messages,
            temperature=0.5
        )
    except openai.error.RateLimitError as e:
        # Invalid billing
        return str(e)
    return str(completions.choices[0]["message"]["content"])


# Slash Commands

@bot.tree.command(name="variation", description='Must be a valid PNG file, less than 4MB, and square')
@app_commands.describe(
    image='What image should I make variation(s) of?',
    private='Whether the image will be visible only to you'
)
async def variation(interaction: discord.Interaction, image: discord.Attachment, private: bool = False):
    await interaction.response.defer(ephemeral=private)
    prompt = await discord.Attachment.read(image)
    embed = discord.Embed(
        title='AI',
        color=random.randint(0, 16777215)
    )
    try:
        variations = image_variation_response(prompt, 1)
        for var in variations:
            embed.set_image(url=var['url'])
            await interaction.followup.send(embed=embed, ephemeral=private)
    except Exception as e:
        print(e)
        await interaction.followup.send("Must be a valid PNG file, less than 4MB, and square")


@bot.tree.command(name="image", description='Ask AI to generate some images')
@app_commands.describe(
    request='What image should I make?',
    private='Whether the image will be visible only to you'
)
async def image(interaction: discord.Interaction, request: str, private: bool = False):
    await interaction.response.defer(ephemeral=private)
    embed = discord.Embed(
        title='AI',
        color=random.randint(0, 16777215),
    )
    try:
        response = image_response(request)
        embed.set_image(url=response)
        await interaction.followup.send(embed=embed, ephemeral=private)
    except:
        await interaction.followup.send("The request was rejected as a result of the AI's safety system.")


@bot.tree.command(name="ai", description='Ask AI some questions')
@app_commands.describe(
    request='What should I do?',
    private='Whether the message will be visible only to you'
)
async def ai(interaction: discord.Interaction, request: str, private: bool = False):
    await interaction.response.defer(ephemeral=private)
    response = ai_response(request)
    # if code_lang != 'False':
    #     response = f'```{code_lang}\n{response}```'
    embed = discord.Embed(
        title='AI',
        description=response,
        color=random.randint(0, 16777215)
    )
    await interaction.followup.send(embed=embed, ephemeral=private)
