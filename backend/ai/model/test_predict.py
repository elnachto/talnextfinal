from predict import predict_candidate

cv_text = """
Senior Flutter developer with 6 years of experience.
Skills: Flutter, Dart, Firebase, REST APIs, Docker.
"""

result = predict_candidate(cv_text)
print(result)