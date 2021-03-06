<#import "template.ftl" as layout>
<@layout.registrationLayout; section>
    <#if section = "header">
        ${msg("registerTitle")}
    <#elseif section = "form">
        <div class="title-container">
            <h1 class="login-title">Inscription</h1>
            <p class="login-subtitle">Déjà un compte ? <a href="${url.loginUrl}">${kcSanitize(msg("backToLogin"))?no_esc}</a></span>
        </div>
        <form id="kc-register-form" class="${properties.kcFormClass!}" action="${url.registrationAction}" method="post">
            
            <div class="${properties.kcFormGroupClass!} ${messagesPerField.printIfExists('email',properties.kcFormGroupErrorClass!)}">
                <input type="text" id="email" class="enkiform__input" name="email" value="${(register.formData.email!'')}" autocomplete="email" required />
                <label for="email" class="enkiform__label">${msg("email")}</label>
            </div>

          <#if !realm.registrationEmailAsUsername>
            <div class="${properties.kcFormGroupClass!} ${messagesPerField.printIfExists('username',properties.kcFormGroupErrorClass!)}">
                <input type="text" id="username" class="enkiform__input" name="username" value="${(register.formData.username!'')}" autocomplete="username" required />
                <label for="username" class="enkiform__label">${msg("username")}</label>
            </div>
          </#if>

            <#if passwordRequired??>
            <div class="${properties.kcFormGroupClass!} ${messagesPerField.printIfExists('password',properties.kcFormGroupErrorClass!)}">
                <input type="password" id="password" class="enkiform__input" name="password" autocomplete="new-password" required/>
                <label for="password" class="enkiform__label">${msg("password")}</label>
            </div>

            <div class="${properties.kcFormGroupClass!} ${messagesPerField.printIfExists('password-confirm',properties.kcFormGroupErrorClass!)}">
                <input type="password" id="password-confirm" class="enkiform__input" name="password-confirm" required />
                <label for="password-confirm" class="enkiform__label">${msg("passwordConfirm")}</label>
            </div>
            </#if>

            <#if recaptchaRequired??>
            <div class="form-group">
                <div class="${properties.kcInputWrapperClass!}">
                    <div class="g-recaptcha" data-size="compact" data-sitekey="${recaptchaSiteKey}"></div>
                </div>
            </div>
            </#if>

            <div class="${properties.kcFormGroupClass!}">
                <div id="kc-form-buttons" class="${properties.kcFormButtonsClass!}">
                    <input class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" type="submit" value="${msg("doRegister")}"/>
                </div>
            </div>
        </form>
    </#if>
</@layout.registrationLayout>
