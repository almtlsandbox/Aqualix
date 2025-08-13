# FIX AUTO-TUNE AU CHARGEMENT D'IMAGE

## 🔍 PROBLÈME IDENTIFIÉ

**Symptôme :** Au premier chargement d'image, même si les auto-tune sont cochés, l'application applique les valeurs par défaut. Il faut désactiver puis réactiver l'auto-tune global pour obtenir le résultat auto-tuned.

**Cause :** L'auto-tune ne se déclenchait que lors d'un changement d'état (toggle), pas au chargement initial d'une image.

## ✅ SOLUTION IMPLÉMENTÉE

### 1. Ajout d'une nouvelle méthode dans `ParameterPanel`
```python
def trigger_auto_tune_for_new_image(self):
    """Trigger auto-tune for all enabled steps when a new image is loaded"""
```

Cette méthode :
- Vérifie qu'une image est disponible
- Trouve tous les steps avec auto-tune activé
- Exécute `_perform_auto_tune_step()` pour chaque step activé
- Met à jour l'interface et déclenche le preview

### 2. Modification de `load_image()` dans `main.py`
```python
# Check if auto-tune is enabled and trigger it for new image
if hasattr(self.param_panel, 'global_auto_tune_var') and self.param_panel.global_auto_tune_var.get():
    # Auto-tune is enabled globally, execute auto-tune for active steps
    self.param_panel.trigger_auto_tune_for_new_image()
```

Ajout après le chargement de l'image et avant `update_preview()`.

## 🎯 COMPORTEMENT ATTENDU MAINTENANT

1. **Au démarrage :** Auto-tune global est coché ✅
2. **Au chargement d'image :** 
   - L'image se charge
   - L'auto-tune se déclenche automatiquement si activé
   - L'utilisateur voit immédiatement le résultat auto-tuned
3. **Toggle manuel :** Continue de fonctionner comme avant

## 📝 FICHIERS MODIFIÉS

- `src/main.py` - Ajout du trigger auto-tune dans `load_image()`
- `src/ui_components.py` - Ajout de `trigger_auto_tune_for_new_image()`

## ✅ VALIDATION

L'auto-tune se déclenche maintenant automatiquement au chargement d'image quand :
- L'auto-tune global est activé (coché par défaut)
- Une image est chargée avec succès
- Des steps individuels ont leur auto-tune activé

Le problème original est résolu ! 🎉
