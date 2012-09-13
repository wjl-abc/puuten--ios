//
//  AFKPageFlipper.m
//  AFKPageFlipper
//
//  Created by Marco Tabini on 10-10-12.
//  Copyright 2010 AFK Studio Partnership. All rights reserved.
//

#import "AFKPageFlipper.h"


#pragma mark -
#pragma mark UIView helpers


@interface UIView(Extended)

- (UIImage *)imageByRenderingView;

@end


@implementation UIView(Extended)


- (UIImage *)imageByRenderingView {
    CGFloat oldAlpha = self.alpha;
    self.alpha = 1.0f;
    UIGraphicsBeginImageContext(self.bounds.size);
	[self.layer renderInContext:UIGraphicsGetCurrentContext()];
	UIImage *resultingImage = UIGraphicsGetImageFromCurrentImageContext();
	UIGraphicsEndImageContext();
    self.alpha = oldAlpha;
	return resultingImage;
}

@end


#pragma mark -
#pragma mark Private interface


@interface AFKPageFlipper()

@property (nonatomic,assign) UIView *currentView;
@property (nonatomic,retain) UIImage *currentImage;

@property (nonatomic,assign) UIView *nextView;
@property (nonatomic,retain) UIImage *nextImage;

@property (nonatomic, assign) UIView *prevView;
@property (nonatomic, retain) UIImage *prevImage;

@end


@implementation AFKPageFlipper

@synthesize panRecognizer = _panRecognizer;
@synthesize currentImage;
@synthesize nextImage;
@synthesize prevImage;

#pragma mark -
#pragma mark Flip functionality


- (void) initFlip {
	// Hide existing views
	self.currentView.alpha = 0.0f;
	self.nextView.alpha = 0.0f;
    self.prevView.alpha = 0.0f;
	
	// Create representational layers
	CGRect rect = self.bounds;
	rect.size.height /= 2;
	
	backgroundAnimationLayer = [CALayer layer];
	backgroundAnimationLayer.frame = self.bounds;
	backgroundAnimationLayer.zPosition = -300000;
	
	CALayer *topLayer = [CALayer layer];
	topLayer.frame = rect;
	topLayer.masksToBounds = YES;
	topLayer.contentsGravity = kCAGravityBottom;
	
	[backgroundAnimationLayer addSublayer:topLayer];
	
	rect.origin.y = rect.size.height;
	
	CALayer *bottomLayer = [CALayer layer];
	bottomLayer.frame = rect;
	bottomLayer.masksToBounds = YES;
	bottomLayer.contentsGravity = kCAGravityTop;
	
	[backgroundAnimationLayer addSublayer:bottomLayer];
	
	if (flipDirection == AFKPageFlipperDirectionDown) {
		topLayer.contents = (id) [prevImage CGImage];
        revealedLayer = topLayer;
		bottomLayer.contents = (id) [currentImage CGImage];
        coveredLayer = bottomLayer;
	} else {
		topLayer.contents = (id) [currentImage CGImage];
        coveredLayer = topLayer;
		bottomLayer.contents = (id) [nextImage CGImage];
        revealedLayer = bottomLayer;
	}
    
	[self.layer addSublayer:backgroundAnimationLayer];
	
	rect.origin.y = 0;
	
	flipAnimationLayer = [CATransformLayer layer];
	flipAnimationLayer.anchorPoint = CGPointMake(0.5, 1.0);
	flipAnimationLayer.frame = rect;
	
	[self.layer addSublayer:flipAnimationLayer];
	
	CALayer *backLayer = [CALayer layer];
	backLayer.frame = flipAnimationLayer.bounds;
	backLayer.doubleSided = NO;
	backLayer.masksToBounds = YES;
	
	[flipAnimationLayer addSublayer:backLayer];
	
	CALayer *frontLayer = [CALayer layer];
	frontLayer.frame = flipAnimationLayer.bounds;
	frontLayer.doubleSided = NO;
	frontLayer.masksToBounds = YES;
	frontLayer.transform = CATransform3DMakeRotation(M_PI, -1.0, 0.0, 0.0);
	
	[flipAnimationLayer addSublayer:frontLayer];
	
	if (flipDirection == AFKPageFlipperDirectionDown) {
		backLayer.contents = (id) [currentImage CGImage];
		backLayer.contentsGravity = kCAGravityBottom;
		
		frontLayer.contents = (id) [prevImage CGImage];
		frontLayer.contentsGravity = kCAGravityTop;
		
		CATransform3D transform = CATransform3DMakeRotation(0.0, -1.0, 0.0, 0.0);
		transform.m34 = 1.0f / 1000.0f;
		
		flipAnimationLayer.transform = transform;
		
		currentAngle = startFlipAngle = 0;
		endFlipAngle = -M_PI;
	} else {
		backLayer.contentsGravity = kCAGravityBottom;
		backLayer.contents = (id) [nextImage CGImage];
		
		frontLayer.contents = (id) [currentImage CGImage];
		frontLayer.contentsGravity = kCAGravityTop;
		
		CATransform3D transform = CATransform3DMakeRotation(-M_PI / 1.1, -1.0, 0.0, 0.0);
		transform.m34 = 1.0f / 1000.0f;
		
		flipAnimationLayer.transform = transform;
		
		currentAngle = startFlipAngle = -M_PI;
		endFlipAngle = 0;
	}
}


- (void)cleanupFlip {
	[backgroundAnimationLayer removeFromSuperlayer];
	[flipAnimationLayer removeFromSuperlayer];
	
	backgroundAnimationLayer = Nil;
	flipAnimationLayer = Nil;
    revealedLayer = Nil;
    coveredLayer = Nil;
	
	
    //  NSLog(@"setNextViewOnCompletion %i", (int)setNextViewOnCompletion);
    //  NSLog(@"animating               %i", (int)animating);
	if (setNextViewOnCompletion) {
		[self.currentView removeFromSuperview];
        if (flipDirection == AFKPageFlipperDirectionUp) {
            if (self.nextView) {
                self.currentView = self.nextView;
            }
        } else {
            if (self.prevView) {
                self.currentView = self.prevView;
            }
        }
		self.nextView = currentPage+1 <= [self.dataSource numberOfPagesForPageFlipper:self] ? [self.dataSource viewForPage:self.currentPage+1 inFlipper:self] : nil;
        self.prevView = currentPage-1 > 0 ? [self.dataSource viewForPage:self.currentPage-1 inFlipper:self] : nil;
	} else {
		[self.nextView removeFromSuperview];
        [self.prevView removeFromSuperview];
	}
    
	self.currentView.alpha = 1.0f;
	animating = NO;
}


- (void)setFlipProgress:(float)progress setDelegate:(BOOL)setDelegate animate:(BOOL)animate {
    if (animating) return;
    if (animate) animating = YES;
    
    float newAngle = startFlipAngle + progress * (endFlipAngle - startFlipAngle);
	float duration = fabs((newAngle - currentAngle) / (endFlipAngle - startFlipAngle));
    if (endFlipAngle == startFlipAngle) duration = 1.0f;
	duration = animate ? MAX(0.2f, duration) : 0.0f;
    
	currentAngle = newAngle;
	
	CATransform3D endTransform = CATransform3DIdentity;
	endTransform.m34 = -1.0f / 1000.0f;
	endTransform = CATransform3DRotate(endTransform, newAngle, 1.0, 0.0, 0.0);
	
	[flipAnimationLayer removeAllAnimations];
    
	[CATransaction begin];
	[CATransaction setAnimationDuration:duration];
	[CATransaction setAnimationTimingFunction:[CAMediaTimingFunction functionWithName:kCAMediaTimingFunctionEaseOut]];
    
	flipAnimationLayer.transform = endTransform;
    revealedLayer.opacity = MIN(1.0f, sqrtf(2.0f*progress));
    coveredLayer.opacity = MIN(1.0, sqrtf(2.0f*(1.0f-progress)));
    
	[CATransaction commit];
	
	if (setDelegate) {
		[self performSelector:@selector(cleanupFlip) withObject:Nil afterDelay:duration];
	}
}


- (void)flipPage {
	[self setFlipProgress:1.0f setDelegate:YES animate:YES];
}

- (void)animateFirstPage {
    [self initFlip];
    double delayInSeconds = 0.01;
    dispatch_time_t popTime = dispatch_time(DISPATCH_TIME_NOW, delayInSeconds * NSEC_PER_SEC);
    dispatch_after(popTime, dispatch_get_main_queue(), ^(void){
        [self setFlipProgress:0.5f setDelegate:NO animate:NO];
        double delayInSeconds = 0.3;
        dispatch_time_t popTime = dispatch_time(DISPATCH_TIME_NOW, delayInSeconds * NSEC_PER_SEC);
        dispatch_after(popTime, dispatch_get_main_queue(), ^(void){
            setNextViewOnCompletion = NO;
            [self setFlipProgress:0.0f setDelegate:YES animate:YES];
        });
    });
}


#pragma mark -
#pragma mark Animation management


- (void)animationDidStop:(NSString *) animationID finished:(NSNumber *) finished context:(void *) context {
	[self cleanupFlip];
}


#pragma mark -
#pragma mark Properties

@synthesize currentView;


- (void)setCurrentView:(UIView *)value {
    [currentView release];
	currentView = [value retain];
    self.currentImage = [currentView imageByRenderingView];
}


@synthesize nextView;


- (void)setNextView:(UIView *)value {
    [nextView release];
	nextView = [value retain];
    self.nextImage = [nextView imageByRenderingView];
}


@synthesize prevView;


- (void)setPrevView:(UIView *)value {
    [prevView release];
	prevView = [value retain];
    self.prevImage = [prevView imageByRenderingView];
}


@synthesize currentPage;


- (BOOL)doSetCurrentPage:(NSInteger)value {
	if (value == currentPage) {
		return FALSE;
	}
	
	flipDirection = value < currentPage ? AFKPageFlipperDirectionDown : AFKPageFlipperDirectionUp;
	
    if (flipDirection == AFKPageFlipperDirectionDown) {
        if (currentPage == 0) self.prevView = [self.dataSource viewForPage:value inFlipper:self];
        [self addSubview:self.prevView];
    } else {
        if (currentPage == 0) self.nextView = [self.dataSource viewForPage:value inFlipper:self];
        [self addSubview:self.nextView];
    }
	
	currentPage = value;
	return TRUE;
}

- (void)setCurrentPage:(NSInteger) value {
	if (![self doSetCurrentPage:value]) {
		return;
	}
	
	setNextViewOnCompletion = YES;
	animating = NO;
	
    if (flipDirection == AFKPageFlipperDirectionDown) {
        self.prevView.alpha = 1.0f;
    } else {
        self.nextView.alpha = 1.0f;
    }
    [self cleanupFlip];
}


- (void) setCurrentPage:(NSInteger) value animated:(BOOL) animated {
	if (![self doSetCurrentPage:value]) {
		return;
	}
	
	setNextViewOnCompletion = YES;
	animating = YES;
	
	if (animated) {
		[self initFlip];
		[self performSelector:@selector(flipPage) withObject:Nil afterDelay:0.001];
	} else {
		[self animationDidStop:Nil finished:[NSNumber numberWithBool:NO] context:Nil];
	}
    
}


@synthesize dataSource;


- (void) setDataSource:(NSObject <AFKPageFlipperDataSource>*) value withPage:(int) page {
	if (dataSource) {
		[dataSource release];
	}
	
	dataSource = [value retain];
	numberOfPages = [dataSource numberOfPagesForPageFlipper:self];
    currentPage = 0;
	self.currentPage = page;
}


@synthesize disabled;


- (void) setDisabled:(BOOL) value {
	disabled = value;
	
	self.userInteractionEnabled = !value;
	
	for (UIGestureRecognizer *recognizer in self.gestureRecognizers) {
		recognizer.enabled = !value;
	}
}


#pragma mark -
#pragma mark Touch management

- (void) panned:(UIPanGestureRecognizer *) recognizer {
	static BOOL hasFailed;
    if (animating) {
        hasFailed = YES;
        return;
    }
    
	static NSInteger oldPage;
    
	float translation = [recognizer translationInView:self].y;
	float progress = translation*1.5f / self.bounds.size.height;
	
	if (flipDirection == AFKPageFlipperDirectionUp) {
		progress = MAX(-1.0f, MIN(progress, 0.0f));
	} else {
		progress = MIN(1.0f, MAX(progress, 0.0f));
	}
	
	switch (recognizer.state) {
		case UIGestureRecognizerStateBegan:
			hasFailed = FALSE;
            
            oldPage = self.currentPage;
            
			if (translation > 0) {
				if (self.currentPage > 1) {
					[self doSetCurrentPage:self.currentPage - 1];
				} else {
					hasFailed = TRUE;
					return;
				}
			} else {
				if (self.currentPage < numberOfPages) {
					[self doSetCurrentPage:self.currentPage + 1];
				} else {
					hasFailed = TRUE;
					return;
				}
			}
			animating = NO;
			setNextViewOnCompletion = NO;
			[self initFlip];
			break;
			
		case UIGestureRecognizerStateChanged:
			if (hasFailed) return;
			setNextViewOnCompletion = NO;
			[self setFlipProgress:MIN(0.95f,fabs(progress)) setDelegate:NO animate:NO];
			break;
			
		case UIGestureRecognizerStateFailed:
            setNextViewOnCompletion = NO;
			[self setFlipProgress:0.0 setDelegate:YES animate:YES];
			currentPage = oldPage;
			break;
			
		case UIGestureRecognizerStateRecognized:
			if (hasFailed) {
				setNextViewOnCompletion = NO;
				[self setFlipProgress:0.0 setDelegate:YES animate:YES];
				currentPage = oldPage;
				return;
			}
            float velocity = [recognizer velocityInView:self].y;
			if (fabsf(velocity) > 1000.0f || fabsf(progress) > 0.5f) {
				setNextViewOnCompletion = YES;
				[self setFlipProgress:1.0f setDelegate:YES animate:YES];
			} else {
				[self setFlipProgress:0.0f setDelegate:YES animate:YES];
				currentPage = oldPage;
			}
			break;
            
		default:
			break;
	}
}


#pragma mark -
#pragma mark Frame management


- (void) setFrame:(CGRect) value {
	super.frame = value;
    
	numberOfPages = [dataSource numberOfPagesForPageFlipper:self];
	
	if (self.currentPage > numberOfPages) {
		self.currentPage = numberOfPages;
	}
	
}


#pragma mark -
#pragma mark Initialization and memory management


+ (Class) layerClass {
	return [CATransformLayer class];
}

- (id)initWithFrame:(CGRect)frame {
    if ((self = [super initWithFrame:frame])) {
		_panRecognizer = [[UIPanGestureRecognizer alloc] initWithTarget:self action:@selector(panned:)];
        [self addGestureRecognizer:_panRecognizer];
    }
    return self;
}


- (void)dealloc {
	[dataSource release];
	[currentView release];
    [currentImage release];
	[nextView release];
    [nextImage release];
    [prevView release];
    [prevImage release];
	[_panRecognizer release];
    
	
	[backgroundAnimationLayer release];
	[flipAnimationLayer release];
    
    [revealedLayer release];
    [coveredLayer release];
    
    [super dealloc];
}


@end
