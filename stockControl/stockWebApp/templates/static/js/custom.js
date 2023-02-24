document.addEventListener('DOMContentLoaded', () => {
  const addIngredientBtn = document.getElementById('add-ingredient')
  const ingredientList = document.getElementById('ingredient-list')

  addIngredientBtn.addEventListener('click', () => {
    const inputGroup = document.querySelector('.input-group')
    const newInputGroup = inputGroup.cloneNode(true)
    const removeBtn = document.createElement('button')
    removeBtn.classList.add('btn', 'btn-danger')
    removeBtn.type = 'button'
    removeBtn.innerHTML = '<i class="bi bi-trash"></i>'
    removeBtn.addEventListener('click', () => {
      newInputGroup.remove()
    })
    newInputGroup.appendChild(removeBtn)
    ingredientList.appendChild(newInputGroup)
  })
})
