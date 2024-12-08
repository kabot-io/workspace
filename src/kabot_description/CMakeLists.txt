cmake_minimum_required(VERSION 3.5)

project(kabot_description)

find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

install(
  DIRECTORY
    models/
  DESTINATION share/${PROJECT_NAME}/models
)

install(
  DIRECTORY
    urdf/
  DESTINATION share/${PROJECT_NAME}/urdf
)

# Generate SDF from XACRO
set(SOURCE_SDF_FILE ${CMAKE_CURRENT_SOURCE_DIR}/models/kabot/model.sdf)
set(XACRO_FILE ${CMAKE_CURRENT_SOURCE_DIR}/urdf/kabot.xacro)
set(URDF_FILE ${CMAKE_CURRENT_BINARY_DIR}/kabot.urdf)
set(SDF_FILE ${CMAKE_CURRENT_BINARY_DIR}/model.sdf)
set(MODEL_CONFIG ${CMAKE_CURRENT_SOURCE_DIR}/models/kabot/model.config)

if(NOT EXISTS ${SOURCE_SDF_FILE})
  message(WARNING "kabot_description/models/kabot/model.sdf not found.\nGenerating from URDF...")

  add_custom_command(
      OUTPUT ${URDF_FILE}
      COMMAND xacro ${XACRO_FILE} -o ${URDF_FILE}
      DEPENDS ${XACRO_FILE}
      COMMENT "Generating URDF from XACRO"
  )

  add_custom_command(
      OUTPUT ${SDF_FILE}
      COMMAND gz sdf -p ${URDF_FILE} > ${SDF_FILE}
      DEPENDS ${URDF_FILE}
      COMMENT "Generating SDF from URDF"
  )

  add_custom_target(generate_files ALL DEPENDS ${SDF_FILE})
  
  install(
      FILES ${SDF_FILE}
      DESTINATION share/${PROJECT_NAME}/models/kabot
  )
else()
    message(WARNING "Using existing kabot_description/models/kabot/model.sdf")
    install(
        FILES ${SOURCE_SDF_FILE}
        DESTINATION share/${PROJECT_NAME}/models/kabot
    )
endif()

install(
    FILES ${MODEL_CONFIG}
    DESTINATION share/${PROJECT_NAME}/models/kabot
)

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.sh.in")

ament_package()
