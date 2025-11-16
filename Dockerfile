FROM eclipse-temurin:17-jre

WORKDIR /app

# Copy the built jar (replace name if you change project name)
# Best practice is to copy from a CI build artifact
COPY build/libs/MemVra-*.jar app.jar

ENV JAVA_OPTS=""
EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar /app/app.jar"]