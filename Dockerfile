# syntax=docker/dockerfile:1

# ---- Build stage ----
FROM gradle:8.10.2-jdk17 AS build
WORKDIR /home/gradle/project

# Copy Gradle configs first for better caching
COPY build.gradle settings.gradle ./
COPY memvra-client-java/build.gradle memvra-client-java/build.gradle

# Copy sources
COPY src src
COPY memvra-client-java/src memvra-client-java/src

# Build the Spring Boot fat jar (skip tests in container build)
RUN gradle clean bootJar -x test

# ---- Runtime stage ----
FROM eclipse-temurin:17-jre
WORKDIR /app

# Optional JVM tuning via JAVA_OPTS
ENV JAVA_OPTS=""

# Copy built jar from build stage
COPY --from=build /home/gradle/project/build/libs/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar /app/app.jar"]